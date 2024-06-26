import mesa
from robots.agents import Waste, Robot, Grid_Tile
from robots.model import RadioactiveEnv


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Grid_Tile:
        portrayal["Shape"] = f"robots/resources/tile_{agent.colour}.png"
        # https://icons8.com/web-app/36821/German-Shepherd
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 0
        portrayal["text_color"] = "Black"

    elif type(agent) is Waste:
        portrayal["Shape"] = f"robots/resources/waste_{agent.colour}.png"
        # https://icons8.com/web-app/433/sheep
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Robot:
        portrayal["Shape"] = f"robots/resources/robot_{agent.colour}.png"
        # https://icons8.com/web-app/36821/German-Shepherd
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text_color"] = "Black"

    # elif type(agent) is GrassPatch:
    #     if agent.fully_grown:
    #         portrayal["Color"] = ["#00FF00", "#00CC00", "#009900"]
    #     else:
    #         portrayal["Color"] = ["#84e184", "#adebad", "#d6f5d6"]
    #     portrayal["Shape"] = "rect"
    #     portrayal["Filled"] = "true"
    #     portrayal["Layer"] = 0
    #     portrayal["w"] = 1
    #     portrayal["h"] = 1

    return portrayal


canvas_element = mesa.visualization.CanvasGrid(wolf_sheep_portrayal, 21, 5, 500, 125)
chart_element = mesa.visualization.ChartModule(
    [
        {"Label": "Waste", "Color": "#AA0000"}
    ]
)

model_params = {
    # # The following line is an example to showcase StaticText.
    # "title": mesa.visualization.StaticText("Parameters:"),
    # "grass": mesa.visualization.Checkbox("Grass Enabled", True),
    # "grass_regrowth_time": mesa.visualization.Slider("Grass Regrowth Time", 20, 1, 50),
    # "initial_sheep": mesa.visualization.Slider(
    #     "Initial Sheep Population", 100, 10, 300
    # ),
    # "sheep_reproduce": mesa.visualization.Slider(
    #     "Sheep Reproduction Rate", 0.04, 0.01, 1.0, 0.01
    # ),
    # "initial_wolves": mesa.visualization.Slider("Initial Wolf Population", 50, 10, 300),
    # "wolf_reproduce": mesa.visualization.Slider(
    #     "Wolf Reproduction Rate",
    #     0.05,
    #     0.01,
    #     1.0,
    #     0.01,
    #     description="The rate at which wolf agents reproduce.",
    # ),
    # "wolf_gain_from_food": mesa.visualization.Slider(
    #     "Wolf Gain From Food Rate", 20, 1, 50
    # ),
    # "sheep_gain_from_food": mesa.visualization.Slider("Sheep Gain From Food", 4, 1, 10),
}

server = mesa.visualization.ModularServer(
    RadioactiveEnv, [canvas_element, chart_element], "Wolf Sheep Predation", model_params
)
server.port = 8521
