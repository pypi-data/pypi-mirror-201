from arklibrary.blueprints import Spectator, PlayerManagement, CreativeMode, ServerManagement
from arklibrary.blueprints import ItemManagement, DinoManagement, Teleportation, Map, TribeManagement
from pathlib import Path
import json


class Admin:
    def __init__(self, driver: 'Driver' = None, password='password', player_id=None):
        # ctrl-x to clear console
        # ctrl-c to copy console
        self.__password = password
        self.__my_player_id = player_id
        self.driver = driver
        self.command_list = []
        self.cache = {'default': player_id}

    def execute(self, *commands):
        if len(self.command_list) > 0:
            self.driver.write_console(*self.command_list, *commands)
            self.command_list.clear()

    def enable_admin(self):
        self.enable_cheats(self.__password)
        self.gcm()
        self.enemy_ignores_me()
        self.execute()
        return self

    def enable_cheats(self, password):
        self.command_list.append(CreativeMode.ENABLE_CHEATS.format(password))
        return self

    def gcm(self):
        self.command_list.append(CreativeMode.GIVE_CREATIVE_MODE)
        return self

    def god_mode(self):
        self.command_list.append(PlayerManagement.GOD)
        return self

    def clear_tutorials(self):
        self.command_list.append(PlayerManagement.CLEAR_TUTORIALS)
        return self

    def leave_me_alone(self):
        self.command_list.append(PlayerManagement.LEAVE_ME_ALONE)
        return self

    def enemy_ignores_me(self, condition=True):
        """ Enemy creatures ignore me """
        condition = "true" if condition else "false"
        self.command_list.append(PlayerManagement.ENEMY_INVISIBLE.format(condition))
        return self

    def ghost(self):
        """ Allows to go through walls """
        self.command_list.append(PlayerManagement.GHOST)
        self.enemy_ignores_me()
        return self

    def enable_spectator(self):
        """ Once you enter the spectator state your body will disapear and your inventory items
        will be erased as well. If you leave the game and rejoin it will carry on where you left
        off, thus using the command "stopspectating" is highly recommended. The latter will
        show the respawn map. """
        self.command_list.append(Spectator.ENABLE_SPECTATOR)
        return self

    def stop_spectating(self):
        """ Stops spectating """
        self.command_list.append(Spectator.STOP_SPECTATING)
        return self

    def message_server(self, message):
        """ Writes to chat as a server message to all players"""
        self.command_list.append(ServerManagement.SERVER_CHAT.format(message))
        return self

    def broadcast(self, message):
        """ Sends a message to the whole server using the banner """
        self.command_list.append(ServerManagement.BROADCAST.format(str(message)))
        return self

    def give_item_to_player(self, player_id, blueprint_path, quantity=1, quality=0, force_blueprint=False):
        """ Adds the specified item (or its blueprint) to the player's inventory in the specified quantity
            Ex. cheat GiveItemToPlayer 696509819 "Blueprint'/Game/PrimalEarth/CoreBlueprints/Weapons/PrimalItemAmmo_AdvancedRifleBullet.PrimalItemAmmo_AdvancedRifleBullet'" 200 1 0
        """
        force_blueprint = 1 if force_blueprint else 0
        self.command_list.append(ItemManagement.GIVE_ITEM_TO_PLAYER.format(
            player_id, blueprint_path, quantity, quality, force_blueprint))
        return self

    def give_items_to_player(self, player_id, blueprint_paths, quantity=1, quality=0, force_blueprint=False):
        """ Adds the specified item (or its blueprint) to the player's inventory in the specified quantity
            Ex. cheat GiveItemToPlayer 696509819 "Blueprint'/Game/PrimalEarth/CoreBlueprints/Weapons/PrimalItemAmmo_AdvancedRifleBullet.PrimalItemAmmo_AdvancedRifleBullet'" 200 1 0
            NOTE: Quantity above the stack limit isn't given
        """
        force_blueprint = 1 if force_blueprint else 0
        for path in blueprint_paths:
            self.command_list.append(ItemManagement.GIVE_ITEM_TO_PLAYER.format(
                player_id, path, quantity, quality, force_blueprint))
        return self

    def spawn_exact_dino(self, dino_blueprint_path="", saddle_blueprint_path="", saddle_quality=0,
                         base_level=150, extra_levels=0, base_stats="0,0,0,0,0,0,1,1",
                         added_stats="0,0,0,0,0,0,0,0", dino_name="", cloned=0, neutered=0,
                         tamed_on="", uploaded_from="", imprinter_name="", imprinter_player_id=0,
                         imprint_quality=0, colors="0,0,0,0,0,0", dino_id=0, exp=0,
                         spawn_distance=0, y_offset=0, z_offset=0):
        """
        DinoBlueprintPath:	    String,	Blueprint path
        SaddleBlueprintPath:	String,	Blueprint path
        To spawn the creature without saddle pass an empty string ("")

        SaddleQuality:	        float,	Quality of the equipped saddle
        BaseLevel:	       Integer[32],	Level of the spawned Dino.
        If the level is not the sum of BaseStats + 1, the creature stats may be broken.

        ExtraLevels:	   Integer[32],	Sum of the domesticated levels
        If the value is not the sum of AddedStats, the creature stats may be broken.

        BaseStats:	            String,	Comma separated string with the base levels
        The order is health, stamina, oxygen, food, weight, melee damage, movement speed, crafting skill
        The set levels will only be visible after putting the creature in and out of a crypod.
        Syntax example: "0,0,0,0,0,0,0,0"

        AddedStats:	            String,	Comma separated string with the domesticated levels
        The order is health, stamina, oxygen, food, weight, melee damage, movement speed, crafting skill
        The set levels will only be visible after putting the creature in and out of a crypod.
        Syntax example: "0,0,0,0,0,0,0,0"

        DinoName:	            String
        Cloned:	            Integer[8]
        Neutered:	        Integer[8]
        TamedOn:	        String
        UploadedFrom:	        String
        ImprinterName:	        String,	If left empty, there will be no imprint
        ImprinterPlayerID:	Integer[32]
        ImprintQuality:	        float

        Colors:     	        String,	Comma separated string with the color ids
        Syntax example: "0,0,0,0,0,0"
        The colors will appear if the creature was put in and out of a cryopod.
        If an empty string ("") is passed, the colors will be randomly taken from the natural occuring colors of that species.

        DinoID:	           Integer[64],	If 0 is passed, the game will roll the id.
        Exp:	           Integer[64]
        spawnDistance:	        float
        YOffset:	            float
        ZOffset:	            float
        """
        format = DinoManagement.SPAWN_EXACT_DINO
        self.command_list.append(format.format(dino_blueprint_path, saddle_blueprint_path, saddle_quality, base_level,
                                   extra_levels, base_stats, added_stats, dino_name, cloned, neutered,
                                   tamed_on,
                                   uploaded_from, imprinter_name, imprinter_player_id, imprint_quality,
                                   colors,
                                   dino_id, exp, spawn_distance, y_offset, z_offset))
        return self

    def spawn_dino(self, blueprint_path, tamed=False, level=0):
        """
        Spawns a dino
        :param name_part:	String	significant part of a creature's Entity ID (without _C)
        :param tamed: 	    Boolean	true or 1: tamed, false or 0: wild
        :param level: 	    float	Give creature a specific level, set to 0 for random

        Ex. spawn_dino("dodo", True, 150)
        """
        tamed = "true" if tamed else "false"
        if 'bionics' in blueprint_path:
            name = blueprint_path.split("/")[-1].split('.')[0]
        else:
            name = blueprint_path.split("/")[4]
        self.command_list.append(DinoManagement.SDF.format(name, tamed, level))
        return self

    def remove_cryosickness(self):
        self.command_list.append(DinoManagement.CLEAR_CRYO_SICKNESS)
        return self

    def set_target_dino_color(self, color_region: int, color_id: int):
        """
        Change a dino's color
        :param color_region:    Integer[32]	Color Region
        :param color_id:        Integer[32]	Color ID.
        """
        self.command_list.append(DinoManagement.SET_TARGET_DINO_COLOR.format(color_region, color_id))
        return self

    def copy_coords(self):
        """ Copies your current coordinates and rotation to clipboard in the form x,y,z Yaw pitch """
        self.command_list.append(Map.COPY_COORDS_TO_CLIPBOARD)
        return self

    def teleport_exact(self, x, y, z, yaw, pitch):
        """ Pitch is looking down or up (-80.00 ... 87.00), and 0.00 is leveled"""
        """ Yaw is rotation left to right (-80.00 north... 0.00 east.. 80.00 south... 179.99 west)"""
        self.command_list.append(Teleportation.SPI.format(int(x), int(y), int(z), float(yaw), float(pitch)))
        return self

    def teleport_gps_coords(self, lattitude, longitude, altitude):
        """ Moves player to GPS coordinates """
        self.command_list.append(Teleportation.TP_COORDS.format(lattitude, longitude, altitude))
        return self

    def teleport_player_id_to_me(self, player_id):
        """
        Teleport player by player id to me
        :param id: int, player's id
        """
        self.command_list.append(Teleportation.TELEPORT_PLAYER_ID_TO_ME.format(player_id))
        return self

    def teleport_to_playerid(self, player_id):
        """ Teleport to another player by their id """

        self.command_list.append(Teleportation.TELEPORT_TO_PLAYER.format(player_id))
        return self

    def paste_teleport(self):
        """ After copying coordinates pastes and teleport here """
        copied = self.driver.app.get_from_clipboard()
        x, y, z, yaw, pitch = copied.split()
        self.command_list.append(Teleportation.SPI.format(int(x), int(y), int(z), float(yaw), float(pitch)))
        return self

    def spawn_beacon(self, blueprint_path):
        self.command_list.append(Map.SUMMON.format(blueprint_path))
        return self

    def teleport_green_obelisk(self):
        """ Teleport myself to green obelisk """

        self.command_list.append(Teleportation.TP.format("green"))
        return self

    def teleport_blue_obelisk(self):
        """ Teleport myself to blue obelisk """

        self.command_list.append(Teleportation.TP.format("blue"))
        return self

    def teleport_red_obelisk(self):
        """ Teleport myself to red obelisk """

        self.command_list.append(Teleportation.TP.format("red"))
        return self

    def teleport_xyz(self, x, y, z):
        """ Moves player to x,y,z game coordinates """
        self.command_list.append(Teleportation.SET_PLAYER_POS.format(x, y, z))
        return self

    def teleport_target_xyz(self, x, y, z):
        """ Moves player or dino to game coordinates """
        self.command_list.append(Teleportation.MOVE_TARGET_TO.format(x, y, z))
        return self

    def save_current_coordinates(self, map, name):
        """ Stores the coordinates into file with a name
        :param name: str, name for the coordinates
        """
        data = {"center": {}, "gen1": {}, "gen2": {}, "island": {},
                "scortched": {}, "ragnarok": {}, "extinction": {}, "aberration": {}}
        if map not in data:
            raise NotImplementedError("'{}' isn't part of the map list: {}".format(map, data.keys()))
        self.copy_coords()
        coords = [float(val) for val in self.driver.get_from_clipboard().split()]
        file_path = Path.cwd() / Path('../logs/saved_coordinates.json')
        if file_path.exists():
            with open(file_path, 'r') as r:
                data = json.load(r)

        cc = {"x": coords[0], "y": coords[1], "z": coords[2], "yaw": coords[3], "pitch": coords[4]}
        data[map][name] = cc
        with open(file_path, "w") as w:
            json.dump(data, w)

    def give_tek_engrams_to(self, player_id, engram=None):
        self.command_list.append(f"cheat GiveTekEngramsTo {player_id} tek")
        return self

    def hide_admin_icon(self, condition=True):
        """ Hides admin icon when writing into chat """
        condition = "true" if condition else "false"
        self.command_list.append("cheat SetAdminIcon {}".format(condition))
        return self

    def tranquilize_target(self):
        """ Tranquilize target in crosshairs """
        self.command_list.append("cheat SetMyTargetSleeping 1")
        return self

    def wake_up_target(self):
        """ Removes tranquilizing effects of target in crosshairs """
        self.command_list.append("cheat SetMyTargetSleeping 0")
        return self

    def add_hexagons(self, amount):
        """ Give myself a number of hexagons """
        self.command_list.append("cheat AddHexagons {}".format(amount))
        return self

    def tame(self):
        """ Tames the targeted dino in my crosshairs """
        self.command_list.append("cheat DoTame")
        return self


    def clear_player_inventory(self, player_id, inventory=True, slot_items=False, equipment=False):
        """ Clears player's inventory, equipped items, and/or slot items.
            Ex. cheat ClearPlayerInventory <playerID> <inventory?> <slotitems?> <equippeditems?>
                cheat ClearPlayerInventory 4213211323 1 1 1 1
        """
        # TODO: Need to fix numbers (e.g. clear_player_inventory(id, True, False, False) -> clear_player_inventory id 1 1 1
        # Should be returning 1 0 0 at the end instead of 1 1 1
        inventory = "1" if inventory else "0"
        slot_items = "1" if inventory else "0"
        equipment = "1" if inventory else "0"

        self.command_list.append(PlayerManagement.CLEAR_PLAYER_INVENTORY.format(player_id, inventory, slot_items, equipment))

    def rename_player(self, current_name, new_name):
        self.command_list.append(PlayerManagement.RENAME_PLAYER.format(current_name, new_name))
        return self

    def rename_tribe(self, current_name, new_name):
        self.command_list.append(TribeManagement.RENAME_TRIBE.format(current_name, new_name))
        return self

    def show_admin_manager(self):
        """ shows a list of all the players with their player id's """
        self.command_list.append(ServerManagement.SHOW_MY_ADMIN_MANAGER)
        return self

    def ban_player(self, player_id):
        """ Bans a player """
        self.command_list.append(ServerManagement.BAN_PLAYER.format(player_id))
        return self

    def unban_player(self, player_id):
        """ Unbans player """
        self.command_list.append(ServerManagement.UNBAN_PLAYER.format(player_id))
        return self

    def disable_spectator(self):
        self.command_list.append(Spectator.STOP_SPECTATING)
        return self

    def teleport(self, command):
        self.command_list.append(Teleportation.TP.format(command))
        return self

    def teleport_king_titan_terminal(self):
        """ Teleport me to King Titan Terminal in Extinction"""

        self.command_list.append(Teleportation.TP.format("king"))
        return self

    def teleport_desert_titan_terminal(self):
        """ Teleport me to Desert Titan Terminal in Extinction"""
        self.command_list.append(Teleportation.TP.format("red"))
        return self

    def teleport_forest_titan_terminal(self):
        """ Teleport me to Forest Titan Terminal in Extinction"""
        self.command_list.append(Teleportation.TP.format("green"))
        return self

    def teleport_ice_titan_terminal(self):
        """ Teleport me to Ice Titan Terminal in Extinction"""
        self.command_list.append(Teleportation.TP.format("blue"))
        return self

    def teleport_to_player_name(self, name):
        """ Teleport to another player by their name """
        self.command_list.append(Teleportation.TELEPORT_TO_PLAYER_NAME.format(name))
        return self

    def teleport_player_name_to_me(self, name):
        """
        Teleport player by name to me.
        :param name: str, player's ingame name
        """
        self.command_list.append(Teleportation.TELEPORT_PLAYER_NAME_TO_ME.format(name))
        return self

    def kill_target(self):
        """ Kills exactly whoever is in my crosshairs """
        self.command_list.append(DinoManagement.DESTROY_MY_TARGET)
        return self

    def destroy_tribes_dinos(self):
        """ Kills all dinos in my crosshairs in its tribe """
        self.command_list.append(DinoManagement.DESTROY_TRIBE_DINOS)
        return self

    def destroy_tribes_dinos_by_id(self, tribe_id):
        """ Kills all tribe's dinos """
        self.command_list.append(TribeManagement.DESTROY_TRIBE_ID.format(tribe_id))
        return self

    def destroy_players_by_tribeid(self, tribe_id):
        """ Destroys all players in a tribe by tribe id """
        self.command_list.append(TribeManagement.DESTROY_TRIBE_ID_PLAYERS.format(tribe_id))
        return self

    def destroy_tribe_by_id(self, tribe_id):
        """ Destroy a tribe by their id """
        self.command_list.append(TribeManagement.DESTROY_TRIBE_ID.format(tribe_id))
        return self

    def destroy_structures_by_tribeid(self, tribe_id):
        """ Destroys all structures in a tribe by tribe id """
        self.command_list.append(TribeManagement.DESTROY_TRIBE_ID_STRUCTURES.format(tribe_id))
        return self

    def destroy_tribe_structures(self):
        """ destroys target tribe's structures """
        self.command_list.append(TribeManagement.DESTROY_TRIBE_STRUCTURES)
        return self

    def destroy_wild_dinos(self):
        """ Destroys all untamed dinos to help with respawns """
        self.command_list.append(DinoManagement.DESTROY_WILD_DINOS)
        return self

    def force_player_to_join_target_tribe(self, player_id):
        """ Force a player to join a tribe i'm targeting with my crosshairs"""
        self.command_list.append(TribeManagement.FORCE_PLAYER_TO_JOIN_TARGET_TRIBE.format(player_id))
        return self

    def force_myself_into_target_tribe(self):
        """ Force myself into a tribe I'm targeting with my crosshairs """
        self.command_list.append(TribeManagement.FORCE_JOIN_TRIBE)
        return self

    def force_myself_tribe_admin(self):
        """ Force myself as tribe admin """
        self.command_list.append(TribeManagement.FORCE_TRIBE_ADMIN)
        return self

    def force_myself_tribe_owner(self):
        """ Force myself as tribe owner """
        self.command_list.append(TribeManagement.FORCE_TRIBE_FOUNDER)
        return self

    def give_experience_to_player(self, player_id, amount, from_tribe_share=False, prevent_sharing_with_tribe=True):
        """ Give a player experience points """
        from_tribe_share = 1 if from_tribe_share else 0
        self.command_list.append(
            PlayerManagement.GIVE_EXP_TO_PLAYER.format(player_id, amount, from_tribe_share,
                                                       prevent_sharing_with_tribe))
        return self

    def add_experience_on_mounted_dino(self, amount, from_tribe_share=False, prevent_sharing_with_tribe=True):
        """ Give experience to a dino you're mounted on """
        from_tribe_share = 1 if from_tribe_share else 0
        prevent_sharing_with_tribe = 1 if prevent_sharing_with_tribe else 0
        self.command_list.append(
            PlayerManagement.ADD_EXPERIENCE.format(amount, from_tribe_share, prevent_sharing_with_tribe))
        return self

    def set_time_of_day(self, hour: int = 8, minute: int = 0, seconds: int = 0):
        self.command_list.append(Map.SET_TIME_OF_DAY.format(hour, minute, seconds))
        return self

    def morning(self):
        return self.set_time_of_day(hour=4, minute=30)

    def daylight(self):
        return self.set_time_of_day(hour=10)

    def dusk(self):
        return self.set_time_of_day(hour=21)

    def night(self):
        return self.set_time_of_day(hour=24)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.execute()

    def restart_application(self):
        self.driver.app.close()
        return Admin(password=self.__password)



