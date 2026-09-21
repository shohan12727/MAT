from manim import *
import numpy as np


class ParabolaScene(Scene):
    def construct(self):

        # -----------------------------
        # TITLE
        # -----------------------------
        title = Text(
            "The Parabola: y = x\u00b2",
            font_size=34
        ).to_edge(UP)

        self.play(Write(title))
        self.wait(1)

        # -----------------------------
        # AXES
        # -----------------------------
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 4, 1],
            x_length=8,
            y_length=5.5,
            axis_config={"include_tip": True},
        ).shift(DOWN * 0.5)

        # Using plain Text (Pango) instead of the default MathTex labels
        # so this scene doesn't require a LaTeX installation at all.
        axes_labels = axes.get_axis_labels(
            x_label=Text("x", font_size=28),
            y_label=Text("y", font_size=28),
        )

        self.play(Create(axes), Write(axes_labels))
        self.wait(0.5)

        # -----------------------------
        # PARABOLA CURVE
        # -----------------------------
        def f(x):
            return x ** 2

        parabola = axes.plot(f, x_range=[-2, 2], color=YELLOW)

        self.play(Create(parabola), run_time=2.5)
        self.wait(0.5)

        # -----------------------------
        # TRACING DOT + TANGENT LINE
        # -----------------------------
        t = ValueTracker(-2)

        dot = always_redraw(
            lambda: Dot(
                axes.c2p(t.get_value(), f(t.get_value())),
                color=RED,
                radius=0.08,
            )
        )

        def tangent_line():
            x0 = t.get_value()
            slope = 2 * x0  # derivative of x^2
            y0 = f(x0)

            x_start, x_end = x0 - 1, x0 + 1
            p_start = axes.c2p(x_start, y0 + slope * (x_start - x0))
            p_end = axes.c2p(x_end, y0 + slope * (x_end - x0))

            return Line(p_start, p_end, color=BLUE)

        tangent = always_redraw(tangent_line)

        slope_label = always_redraw(
            lambda: Text(
                f"slope = {2 * t.get_value():.1f}",
                font_size=30,
            ).to_corner(UR).shift(DOWN * 1.2 + LEFT * 0.3)
        )

        self.play(FadeIn(dot), Create(tangent), Write(slope_label))
        self.play(
            t.animate.set_value(2),
            run_time=6,
            rate_func=linear,
        )
        self.wait(0.5)

        self.play(FadeOut(tangent), FadeOut(slope_label))

        # -----------------------------
        # FOCUS + DIRECTRIX  (for y = x^2, 4p = 1 -> p = 0.25)
        # -----------------------------
        p = 0.25
        focus_point = axes.c2p(0, p)
        focus_dot = Dot(focus_point, color=GREEN)
        focus_label = Text("focus", font_size=24, color=GREEN).next_to(focus_dot, RIGHT, buff=0.2)

        directrix = DashedLine(
            axes.c2p(-2.5, -p),
            axes.c2p(2.5, -p),
            color=GREEN,
        )
        directrix_label = Text("directrix", font_size=24, color=GREEN).next_to(directrix, DOWN, buff=0.2)

        self.play(
            FadeIn(focus_dot),
            Write(focus_label),
            Create(directrix),
            Write(directrix_label),
        )
        self.wait(2)


class ParabolaEpicyclesWave(Scene):
    """
    A parabola isn't periodic, so true epicycles don't apply directly.
    This scene instead builds a PERIODIC parabolic wave (a repeating
    arc of x^2 clipped and tiled) out of its Fourier series, drawn with
    rotating vectors -- same visual language as the square-wave scene.
    Fourier series of f(x) = x^2 on [-pi, pi], period 2*pi:
        f(x) = pi^2/3 + sum_{n=1}^inf (-1)^n * 4/n^2 * cos(n*x)
    """

    def construct(self):
        title = Text(
            "Fourier Series: A Parabolic Wave from Circles",
            font_size=32
        ).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        N = 6            # number of harmonics
        scale = 0.4      # shrinks amplitude to fit the frame
        origin = LEFT * 4.8
        wave_speed = 0.55

        def coeff(n):
            return ((-1) ** n) * 4 / (n ** 2) * scale

        dc_offset = (PI ** 2 / 3) * scale

        circles = VGroup()
        vectors = VGroup()
        current_point = origin + UP * dc_offset

        # DC term as a fixed offset arrow (not a rotating circle)
        dc_vector = Line(origin, current_point)
        vectors.add(dc_vector)

        for n in range(1, N + 1):
            r = abs(coeff(n))
            circle = Circle(radius=r, stroke_opacity=0.6)
            circle.move_to(current_point)
            vector = Line(current_point, current_point + UP * r)
            circles.add(circle)
            vectors.add(vector)
            current_point = current_point + UP * r

        def epicycle_point(t):
            point = origin.copy() + UP * dc_offset
            for n in range(1, N + 1):
                c = coeff(n)
                point += np.array([c * np.cos(n * t) * 0, c * np.cos(n * t), 0]) \
                    if False else np.array([0, 0, 0])  # placeholder, replaced below
            return point

        # Proper epicycle_point: each harmonic contributes a vector that
        # rotates with the SAME angle convention used to build `circles`
        # above (stacked purely vertically at t=0, i.e. angle = PI/2 at start)
        def epicycle_point(t):
            point = origin.copy()
            point += UP * dc_offset
            for n in range(1, N + 1):
                c = coeff(n)
                r = abs(c)
                sign = 1 if c >= 0 else -1
                angle = n * t + (PI / 2) * (1 if sign > 0 else -1)
                point += np.array([r * np.cos(angle), r * np.sin(angle), 0])
            return point

        self.play(
            LaggedStart(*[Create(c) for c in circles], lag_ratio=0.15),
            run_time=2.5,
        )

        wave = VMobject()
        wave.set_points_as_corners([epicycle_point(0), epicycle_point(0)])
        time = ValueTracker(0)

        def update_wave(mob):
            t_val = time.get_value()
            points = []
            for x in np.linspace(0, t_val, 500):
                p = epicycle_point(x)
                points.append(np.array([p[0] + x * wave_speed, p[1], 0]))
            if len(points) > 1:
                mob.set_points_smoothly(points)

        wave.add_updater(update_wave)
        self.add(wave)

        def update_vectors(group):
            t_val = time.get_value()
            point = origin.copy()
            group[0].put_start_and_end_on(point, point + UP * dc_offset)
            point = point + UP * dc_offset
            for i, n in enumerate(range(1, N + 1), start=1):
                c = coeff(n)
                r = abs(c)
                sign = 1 if c >= 0 else -1
                angle = n * t_val + (PI / 2) * (1 if sign > 0 else -1)
                new_point = point + np.array([r * np.cos(angle), r * np.sin(angle), 0])
                group[i].put_start_and_end_on(point, new_point)
                point = new_point

        vectors.add_updater(update_vectors)
        self.add(vectors)

        dot = Dot(epicycle_point(0), radius=0.08)
        dot.add_updater(lambda d: d.move_to(epicycle_point(time.get_value())))
        self.add(dot)

        self.play(time.animate.set_value(4 * PI), run_time=14, rate_func=linear)

        wave.clear_updaters()
        vectors.clear_updaters()
        dot.clear_updaters()
        self.wait(2)
        