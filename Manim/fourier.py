from manim import *
import numpy as np


class FourierEpicycles(Scene):
    def construct(self):

        # -----------------------------
        # TITLE
        # -----------------------------
        title = Text(
            "Fourier Series: Building a Wave from Circles",
            font_size=34
        ).to_edge(UP)

        self.play(Write(title))
        self.wait(1)

        # -----------------------------
        # PARAMETERS
        # -----------------------------
        N = 9
        # Reduced from 1.8 -> 1.3. The vertical stack of circle radii sums to
        # about 2.275 * radius, so at 1.8 the total amplitude (~4.1) exceeded
        # the frame's half-height (4.0) both for the circle stack and the
        # wave's y-oscillation. At 1.3 the amplitude (~2.96) comfortably fits.
        radius = 1.3
        # Slowed from 1.5 -> 0.55, and moved further left, so the wave's
        # horizontal travel (speed * t_max) plus its x-oscillation no longer
        # runs past the frame's right edge (~7.1).
        wave_speed = 0.55

        # Starting point (moved further left + no longer needs a manual
        # vertical shift now that amplitude is smaller and self-centers)
        origin = LEFT * 4.8

        circles = VGroup()
        vectors = VGroup()

        # -----------------------------
        # CREATE EPICYCLES
        # -----------------------------
        current_point = origin

        for n in range(1, N + 1, 2):

            r = radius * (4 / (PI * n))

            circle = Circle(
                radius=r,
                stroke_opacity=0.7
            )

            circle.move_to(current_point)

            vector = Line(
                current_point,
                current_point + UP * r
            )

            circles.add(circle)
            vectors.add(vector)

            current_point = current_point + UP * r

        # -----------------------------
        # REAL FOURIER FUNCTIONS
        # -----------------------------
        def epicycle_point(t):

            point = origin.copy()

            for n in range(1, N + 1, 2):

                r = radius * (4 / (PI * n))

                point += np.array([
                    r * np.cos(n * t),
                    r * np.sin(n * t),
                    0
                ])

            return point

        # -----------------------------
        # ANIMATED CIRCLES
        # -----------------------------
        self.play(
            LaggedStart(
                *[Create(c) for c in circles],
                lag_ratio=0.15
            ),
            run_time=3
        )

        # -----------------------------
        # WAVE
        # -----------------------------
        wave = VMobject()

        wave.set_points_as_corners([
            epicycle_point(0),
            epicycle_point(0)
        ])

        time = ValueTracker(0)

        def update_wave(mob):

            t = time.get_value()

            points = []

            for x in np.linspace(0, t, 500):

                p = epicycle_point(x)

                # Move horizontally with time (slowed down so it stays on screen)
                x_position = p[0] + (x * wave_speed)

                points.append(
                    np.array([
                        x_position,
                        p[1],
                        0
                    ])
                )

            if len(points) > 1:
                mob.set_points_smoothly(points)

        wave.add_updater(update_wave)

        self.add(wave)

        # -----------------------------
        # ROTATING VECTORS
        # -----------------------------
        def update_vectors(group):

            t = time.get_value()

            point = origin.copy()

            for i, n in enumerate(range(1, N + 1, 2)):

                r = radius * (4 / (PI * n))

                new_point = point + np.array([
                    r * np.cos(n * t),
                    r * np.sin(n * t),
                    0
                ])

                group[i].put_start_and_end_on(
                    point,
                    new_point
                )

                point = new_point

        vectors.add_updater(update_vectors)

        self.add(vectors)

        # -----------------------------
        # TRACE POINT
        # -----------------------------
        dot = Dot(
            epicycle_point(0),
            radius=0.08
        )

        def update_dot(d):

            d.move_to(epicycle_point(time.get_value()))

        dot.add_updater(update_dot)

        self.add(dot)

        # -----------------------------
        # ANIMATE
        # -----------------------------
        self.play(
            time.animate.set_value(4 * PI),
            run_time=12,
            rate_func=linear
        )

        # -----------------------------
        # CLEAN UP
        # -----------------------------
        wave.clear_updaters()
        vectors.clear_updaters()
        dot.clear_updaters()

        self.wait(2)