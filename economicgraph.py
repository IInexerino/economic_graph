from manim import *

class EconomicGraph(Scene):
    def construct(self):
        # Title
        title = Text("Economic Analysis of Mechanization", font_size=40)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        # Axes for the bar chart
        axes = Axes(
            x_range=[0, 2, 1],
            y_range=[0, 400, 50],
            x_length=4,
            y_length=6,
            axis_config={"color": WHITE},
            y_axis_config={"numbers_to_include": range(0, 400, 50)},
        ).to_edge(LEFT)

        # Add labels to axes
        axes_labels = axes.get_axis_labels(x_label="x", y_label="Value")
        self.play(Create(axes), Write(axes_labels))
        self.wait(1)

        # Data for each state
        state_data = {
            "A": [100, 100, 100, 0],
            "B": [120, 80, 100, 20],
            "C": [120, 60, 100, 0],
            "D": [108, 60, 100, 0],
            "E": [108, 54, 108, 0],
        }

        state_details = {
            "A": "A - Firm before the adoption of the machine.",
            "B": "B - After the introduction of the machine:\n- Machine costs 20,\n- 4 out of 10 workers laid off, lower wage bill of 40,\n- Selling at market price there is an additional profit of 20,\n- Growth of surplus-value and profit.",
            "C": "C - Mechanisation extended to all firms:\n- Market price falls and the surplus-profit disappears,\n- The rate of profit falls.",
            "D": "D - Mechanisation extended to sectors producing constant capital:\n- Rate of profit rises again,\n- Cost and market price still decrease.",
            "E": "E - Mechanisation extended to consumer goods sector:\n- Variable capital and necessary labour reduced,\n- Surplus-value and its rate increase,\n- Profit and the rate of profit increase again."
        }

        economic_indicators = {
            "A": [100, 50, 10, 15],
            "B": [166, 66, 9, 14],
            "C": [166, 55, 8.4, 13.8],
            "D": [166, 59, 8.1, 13.8],
            "E": [196, 65, 8.1, 13.8],
        }

        indicators_labels = [
            "Rate of Surplus-Value %:", "Rate of Profit %:", 
            "Production Cost per Unit:", "Consumer Price per Unit:"
        ]

        # Economic indicators positioned to the left of the legend and aligned
        indicator_text = VGroup(*[
            Text(f"{label}", font_size=20).set_color(WHITE)
            for label in indicators_labels
        ]).arrange(DOWN, aligned_edge=LEFT).to_corner(UP + RIGHT, buff=0.75).shift(LEFT * 0.35)

        indicator_values = VGroup(*[
            Text("", font_size=20).set_color(YELLOW)
            for _ in indicators_labels
        ]).arrange(DOWN, aligned_edge=LEFT).next_to(indicator_text, RIGHT, buff=0.5)

        self.play(FadeIn(indicator_text), FadeIn(indicator_values))

        # Colors for bar sections
        colors = [BLUE, TEAL, GREEN, YELLOW]
        labels = ["Constant Capital", "Variable Capital", "Surplus Value", "Surplus Profit"]

        # Legend stays in the current position
        legend = VGroup(
            *[
                VGroup(
                    Square(side_length=0.3, color=color).set_fill(color, opacity=1),
                    Text(label, font_size=20)
                ).arrange(RIGHT, buff=0.5)
                for color, label in zip(colors, labels)
            ]
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UP + RIGHT, buff=0.75).shift(LEFT * 4.5)

        self.play(FadeIn(legend))

        # Bar holder
        bar = VGroup()
        self.add(bar)

        # Function to update the bar
        def update_bar(state):
            bar_components = []
            data = state_data[state]
            y_offset = 0

            for value, color in zip(data, colors):
                if value > 0:
                    rect = Rectangle(
                        width=axes.c2p(0.8, 0)[0] - axes.c2p(0.2, 0)[0],
                        height=axes.c2p(0, value)[1] - axes.c2p(0, 0)[1],
                        color=color,
                    ).set_fill(color, opacity=1).move_to(
                        axes.c2p(1, y_offset + value / 2, 0)
                    )
                    value_text = Text(str(value), font_size=20, color=BLACK).move_to(rect)
                    y_offset += value
                    bar_components.append(VGroup(rect, value_text))

            return VGroup(*bar_components)

        # Lines from bar to y-axis
        def add_lines(state):
            lines = VGroup()
            y_offset = 0

            for value, color in zip(state_data[state], colors):
                if value > 0:
                    line = DashedLine(
                        start=axes.c2p(1, y_offset + value),
                        end=axes.c2p(0, y_offset + value),
                        color=color,
                    )
                    lines.add(line)
                    y_offset += value

            return lines
        
        # Function to display text description slightly further right
        def display_description(state):
            description = Text(
                state_details[state], font_size=16, line_spacing=1.2
            ).to_edge(DR)
            return description

        # Animate through states
        for state in ["A", "B", "C", "D", "E"]:
            new_bar = update_bar(state)
            lines = add_lines(state)
            description = display_description(state)

            # Update economic indicator values dynamically
            indicator_data = economic_indicators[state]
            updated_values = VGroup(*[
                Text(f"{value}", font_size=20).set_color(YELLOW)
                for value in indicator_data
            ]).arrange(DOWN, aligned_edge=LEFT).next_to(indicator_text, RIGHT, buff=0.5)

            self.play(Transform(bar, new_bar), Create(lines), Write(description), 
                      Transform(indicator_values, updated_values))
            self.wait(5)
            self.play(FadeOut(description), Uncreate(lines))

        # Final Description
        final_text = Text(
            "Mechanisation reduces costs and increases surplus-value,\n"
            "but falling prices can offset profitability gains initially.",
            font_size=16
        ).to_edge(DR)

        self.play(Write(final_text))
        self.wait(10)
        self.play(FadeOut(bar), FadeOut(axes), FadeOut(axes_labels), 
                  FadeOut(final_text), FadeOut(legend), FadeOut(indicator_text), FadeOut(indicator_values))
