"""Functions to to generate game stats based on snapshots from a demofile.
"""

from awpy.types import GameFrame


def generate_vector_state(frame: GameFrame, map_name: str) -> dict:
    """Returns a game state in a dictionary format.

    Args:
        frame (GameFrame) : Dict output of a frame generated from the DemoParser class
        map_name (string): String indicating the map name

    Returns:
        A dict with keys for each feature.
    """
    game_state: dict = {}
    game_state["mapName"] = map_name
    game_state["secondsSincePhaseStart"] = frame["seconds"]
    game_state["bombPlanted"] = frame["bombPlanted"]
    game_state["bombsite"] = frame["bombsite"]
    game_state["totalSmokes"] = len(frame["smokes"] or [])
    game_state["totalFires"] = len(frame["fires"] or [])

    # Team specific info (CT)
    game_state["ctAlive"] = 0
    game_state["ctHp"] = 0
    game_state["ctArmor"] = 0
    game_state["ctHelmet"] = 0
    game_state["ctEq"] = 0
    game_state["ctUtility"] = 0
    game_state["ctEqValStart"] = 0
    game_state["ctBombZone"] = 0
    game_state["defusers"] = 0
    for p in frame["ct"]["players"] or []:
        game_state["ctEqValStart"] += p["equipmentValueFreezetimeEnd"]
        if p["isAlive"]:
            game_state["ctAlive"] += 1
            game_state["ctHp"] += p["hp"]
            game_state["ctArmor"] += p["armor"]
            game_state["ctHelmet"] += p["hasHelmet"]
            game_state["ctEq"] += p["equipmentValue"]
            game_state["ctUtility"] += p["totalUtility"]
            game_state["defusers"] += p["hasDefuse"]
            # This does not seem to work correctly
            # It is never filled in parse_demo.go
            if p["isInBombZone"]:
                game_state["ctBombZone"] += 1

    # Team specific info (T)
    game_state["tAlive"] = 0
    game_state["tHp"] = 0
    game_state["tArmor"] = 0
    game_state["tHelmet"] = 0
    game_state["tEq"] = 0
    game_state["tUtility"] = 0
    game_state["tEqValStart"] = 0
    game_state["tHoldingBomb"] = 0
    game_state["tBombZone"] = 0
    for p in frame["t"]["players"] or []:
        game_state["tEqValStart"] += p["equipmentValueFreezetimeEnd"]
        if p["isAlive"]:
            game_state["tAlive"] += 1
            game_state["tHp"] += p["hp"]
            game_state["tArmor"] += p["armor"]
            game_state["tHelmet"] += p["hasHelmet"]
            game_state["tEq"] += p["equipmentValue"]
            game_state["tUtility"] += p["totalUtility"]
            # This does not seem to work correctly
            # It is never filled in parse_demo.go
            if p["isInBombZone"]:
                game_state["tBombZone"] += 1
            if p["hasBomb"]:
                game_state["tHoldingBomb"] = 1

    return game_state


def generate_graph_state(frame: GameFrame) -> dict:
    """Returns a game state as a graph

    Args:
        frame (GameFrame) : Dict output of a frame generated from the DemoParser class

    Returns:
        A dict with keys "T", "CT" and "Global", where each entry is a vector. Global vector is CT + T concatenated
    """
    return {"ct": [], "t": [], "global": []}


def generate_set_state(frame: GameFrame) -> dict:
    """Returns a game state as a set

    Args:
        frame (GameFrame) : Dict output of a frame generated from the DemoParser class

    Returns:
        A dict with keys "T", "CT" and "Global", where each entry is a vector. Global vector is CT + T concatenated
    """
    return {"ct": [], "t": [], "global": []}
