from horsetalk import Disaster, FinishingPosition, FormBreak


class FormFigures:
    @staticmethod
    def parse(form_figures: str):
        return [
            FinishingPosition(int(figure))
            if figure.isdigit()
            else FormBreak(figure)
            if figure in [member.value for member in FormBreak]
            else Disaster[figure]
            for figure in form_figures
        ]
