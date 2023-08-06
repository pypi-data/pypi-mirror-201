from trainerbase.gameobject import GameObject


Number = int | float


class Teleport:
    def __init__(
        self,
        player_x: GameObject,
        player_y: GameObject,
        player_z: GameObject,
        labels: dict[str, tuple[Number, Number, Number]] = None,
    ):
        self.player_x = player_x
        self.player_y = player_y
        self.player_z = player_z
        self.labels = {} if labels is None else labels

    def set_coords(self, x: Number, y: Number, z: Number = 100):
        self.player_x.value = x
        self.player_y.value = y
        self.player_z.value = z

    def get_coords(self):
        return self.player_x.value, self.player_y.value, self.player_z.value

    def goto(self, label: str):
        self.set_coords(*self.labels[label])


def regenerate(current_value: GameObject, max_value: GameObject, percent: Number, min_value: Number = 1):
    if current_value.value < max_value.value:
        current_value.value += max(round(max_value.value * percent / 100), min_value)
