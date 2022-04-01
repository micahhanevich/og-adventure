import cmd
import sys
import os


class Item:
    def __init__(self, desc: str, movable: bool, extDescription: str):
        self.description = desc
        self.movable = movable
        self.extDescription = extDescription


class Equipment(Item):
    def __init__(self, desc: str, extDescription: str, deadliness: int, equip: str):
        super().__init__(desc, True, extDescription)
        self.deadliness = deadliness
        self.equipSlot = equip


class Creature:
    def __init__(self, desc: str, killable: bool, extDescription: str, deadliness: int, reward: Item):
        self.description = desc
        self.killable = killable
        self.extDescription = extDescription
        self.deadliness = deadliness
        self.reward = reward


class Trap(Creature):
    def __init__(self, desc: str, killable: bool, deadliness: int, reward: Item, deathtype: str):
        super().__init__(desc, killable, None, deadliness, None)
        self.deathtype = deathtype


class Location:
    def __init__(self, desc: str, features: list, items: list, creatures: list):
        self.description = desc
        self.features = features
        self.items = items
        self.creatures = creatures
        self.north = None
        self.south = None
        self.east = None
        self.west = None
        self.up = None
        self.down = None
        self.trap = None


class World:
    def __init__(self):

        self.princess = False

        # Item Creator
        self.small_stone = Item('a small stone', True, "A small, unimportant pebble. Don't trip!")
        self.cell_key = Item('a cell key', True,
                             "A large, cast metal key you got from a rat. Would fit in a cell door's lock.")
        self.discarded_flask = Item('a discarded flask', True,
                                    "An old, empty flask. Appears to have been filled with some type of emerald, healing liquid.")
        self.dragon_heart = Item('the heart of a dragon', True,
                                 "The heart of the golden dragon gaurding the princess and the library of secrets. A testament to your strength.")
        self.princess = Item('the helpless (and beautiful!) princess', True,
                             'The fearless princess of the kingdom. You saved her from the golden dragon!')

        self.fountain = Item('a small, unremarkable fountain', False,
                             "A small fountain that protrudes out of rough stone. The water comes from seemingly nowhere, and pours endlessly and pointlessly into cracks in the rock.")
        self.beast_well = Item('an intricate well filled with some sparkling liquid', False,
                               "Before you can control yourself, you suddenly lunge forward and take a deep gulp from the well.")
        self.tri_decor = Item('three golden triangles hanging on the wall', False,
                              "The bottom-right triangle glows brighter the close you get. Also, is that a secret passage to the north...?")
        self.bonfire = Item('a small bonfire', False, "BONFIRE LIT!")
        self.nibble = Item('the nibble of a large rat on your toe', False,
                           'The nibble on your foot is coming from a large rat.')

        # Equipment Creator
        self.ruined_shirt = Equipment('a ragged shirt',
                                      'A nearly shredded, previously white shirt. Nothing more than rags, but better than being naked.',
                                      0, 'chest')
        self.ruined_shorts = Equipment('a pair of ratty shorts',
                                       'Badly torn brown shorts. They give no protection, but better than being nude.',
                                       0, 'legs')
        self.guard_sword = Equipment('a guard sword',
                                     "A decently crafted, sharp blade commonly used by the castle guards.", 2, 'hand')
        self.hero_sword = Equipment('the sword that seals the darkness',
                                    "An ancient, immensely powerful sword, previously lost to time.", 3, 'hand')

        # Creature Creator
        self.cell_rat = Creature('a large rat nibbling on your toe', True,
                                 "A very large, very slimy rat. Currently occupied with nibbling on your big toe.", 0,
                                 self.cell_key)
        self.fairy = Creature('a small creature glowing blue and flying out of reach', False,
                              "Further inspection reveals nothing- it's too high to see well.", 0, None)
        self.hall_guard = Creature('a sleeping guard', True,
                                   "A musuclar guard in full armor. Despite his threatening form and large sword, he is currently asleep.",
                                   2, self.guard_sword)
        self.dragon = Creature('a golden dragon', True,
                               "An enormous, fire-breathing dragon coated in golden scales. Only the strongest weapon can pierce its scales.",
                               3, self.dragon_heart)

        # Location Creator
        self.dungeon_cell = Location('in a damp, moldy dungeon',
                                     [
                                         # Features
                                         'There is a trickle coming out of a hole in the ceiling, next to the north wall.',
                                         'The water from the trickle goes down an open grate into the darkness.',
                                         'You can see flickering light under the cell door on the south wall, and hear snoring outside.',
                                         '...Also, it feels like something is nibbling on your toe.'
                                     ],
                                     [
                                         # Items
                                         self.nibble
                                     ],
                                     [
                                         # Creatures
                                         self.cell_rat
                                     ])

        self.prison_hall = Location('in a short hallway lined with locked cells',
                                    [
                                        # Features
                                        'There is a guard sleeping on the west end of the hall.',
                                        'There is a spiral staircase at the west end of the hall.',
                                        'There is a door to the east with sounds coming from the other side.',
                                        'The north cell door you came from remains open.'
                                    ],
                                    [
                                        # Items
                                        self.small_stone
                                    ],
                                    [
                                        # Creatures
                                        self.hall_guard
                                    ]
                                    )

        self.hall_of_guards = Location('in a large hall. Full of guards. They immediately notice you and attack',
                                       [
                                           # Features
                                       ],
                                       [
                                           # Items
                                       ],
                                       [
                                           # Creatures
                                       ]
                                       )

        self.cathedral = Location('in an old, dilapidated cathedral',
                                  [
                                      # Features
                                      'There are shadowy doorways to the north and south.',
                                      'The north doorway is boarded off, however.',
                                      'There is a trickle of water going down into a dark hole.',
                                      'A spiral staircase descends downwards to the east and curves right.'
                                  ],
                                  [
                                      # Items
                                      self.small_stone
                                  ],
                                  [
                                      # Creatures
                                  ]
                                  )

        self.choice_1 = Location('in a courtyard open to the sky',
                                 [
                                     'On the west wall, there is a large wooden door marked with the word "WOLF".',
                                     'On the east wall, there is a large wooden door marked with the word "RABBIT".',
                                     'On the south wall, there is a large wooden door marked with the word "SNAKE".',
                                     'The north wall contains the dark opening to the cathedral.'
                                     # Features
                                 ],
                                 [
                                     # Items
                                     self.fountain
                                 ],
                                 [
                                     # Creatures
                                 ]
                                 )

        self.choice_2 = Location('in a second courtyard open to the sky',
                                 [
                                     'On the north wall, there is a large wooden door marked with the word "COURAGE".',
                                     'On the east wall, there is a large wooden door marked with the word "UNDEATH".',
                                     'On the south wall, there is a large wooden door marked with the word "TRUTH".',
                                     'The west door is marked with the word "FOOLISHNESS".'
                                     # Features
                                 ],
                                 [
                                     # Items
                                     self.fountain
                                 ],
                                 [
                                     # Creatures
                                 ]
                                 )

        self.bonfire_lit = Location('in a small, roofed-in courtyard',
                                    [
                                        # Features
                                        'There is a small, unlit bonfire in the center of the room.'
                                    ],
                                    [
                                        # Items
                                        self.bonfire,
                                        self.small_stone
                                    ],
                                    [
                                        # Creatures
                                    ]
                                    )

        self.well_of_beasts = Location('in what seems to be a small cave',
                                       [
                                           # Features
                                           'There is a small, but extremely intricate well in the middle of the room.',
                                           'Other than the well, the room seems empty and harmless...'
                                       ],
                                       [
                                           # Items
                                           self.beast_well,
                                           self.small_stone
                                       ],
                                       [
                                           # Creatures
                                       ]
                                       )

        self.treasure_room = Location('in a tall room with vaulted ceilings and stained glass windows',
                                      [
                                          # Features
                                          'There is an enourmous mural on the west wall depicting some ancient battle between an old evil and two reborn heroes.',
                                          'The east wall has the priviledge of having an ornate, gem-encrusted door.',
                                          'The north wall has nothing but three golden triangles and a conspicuous concave wall.'
                                      ],
                                      [
                                          # Items
                                          self.tri_decor
                                      ],
                                      [
                                          # Creatures
                                          self.fairy
                                      ]
                                      )

        self.ttemple = Location(
            'in a dark room. The roof extends upwards into darkness, but something is glowing in the center of the room',
            [
                # Features
                "That's when you see it. A beautiful, blue, ancient sword, glowing with the power of legends.",
                'You feel yourself being drawn to it.'
            ],
            [
                # Items
                self.hero_sword,
                self.small_stone
            ],
            [
                # Creatures
            ]
            )

        self.choice_3 = Location('in an enormous, well-gardened courtyard.',
                                 [
                                     # Features
                                     'In the south wall is an enormous door, softly etched with the word "AIR".'
                                     'In the west wall is an enormous door, pristinely carved with the word "FIRE".'
                                     'In the east wall is an enormous door, deeply etched with the word "EARTH".'
                                 ],
                                 [
                                     # Items
                                 ],
                                 [
                                     # Creatures
                                 ]
                                 )

        self.falldeath = Location('falling for a very long time before you land with a SPLAT',
                                  [
                                      # Features
                                  ],
                                  [
                                      # Items
                                  ],
                                  [
                                      # Creatures
                                  ]
                                  )

        self.mimic_room = Location('in a room with a large treasure chest! You quickly run towards it, but..',
                                   [
                                       # Features
                                   ],
                                   [
                                       # Items
                                   ],
                                   [
                                       # Creatures
                                   ]
                                   )

        self.dragon_hall = Location('in a large, long hall with a gate at the west end',
                                    [
                                        # Features
                                        'A golden-plated dragon blocks the west gate.'
                                    ],
                                    [
                                        # Items
                                        self.small_stone
                                    ],
                                    [
                                        # Creatures
                                        self.dragon
                                    ]
                                    )

        self.princess_cell = Location('in a small chamber the princess calls home',
                                      [
                                          # Features
                                      ],
                                      [
                                          # Items
                                          self.princess
                                      ],
                                      [
                                          # Creatures
                                      ]
                                      )

        self.end = Location('',
                            [
                                # Features
                            ],
                            [
                                # Items
                                self.small_stone
                            ],
                            [
                                # Creatures
                            ]
                            )

        self.blank = Location('copy me',
                              [
                                  # Features
                              ],
                              [
                                  # Items
                              ],
                              [
                                  # Creatures
                              ]
                              )

        # Set up exits
        self.dungeon_cell.south = self.prison_hall
        self.dungeon_cell.up = self.cathedral
        self.dungeon_cell.down = self.falldeath
        # self.dungeon_cell.down = self.ruins

        self.prison_hall.north = self.dungeon_cell
        self.prison_hall.west = self.cathedral
        self.prison_hall.east = self.hall_of_guards

        self.cathedral.south = self.choice_1
        self.cathedral.west = self.prison_hall
        self.cathedral.down = self.dungeon_cell

        self.choice_1.north = self.cathedral
        self.choice_1.south = self.well_of_beasts
        self.choice_1.west = self.hall_of_guards
        self.choice_1.east = self.choice_2

        self.beast_well.north = self.choice_1

        self.choice_2.north = self.treasure_room
        self.choice_2.south = self.choice_3
        self.choice_2.west = self.choice_1
        self.choice_2.east = self.bonfire_lit

        self.bonfire_lit.west = self.choice_2

        self.treasure_room.north = self.ttemple
        self.treasure_room.south = self.choice_2
        self.treasure_room.east = self.mimic_room

        self.ttemple.south = self.treasure_room

        self.choice_3.north = self.choice_2
        self.choice_3.south = self.falldeath
        self.choice_3.west = self.dragon_hall
        self.choice_3.east = self.end

        self.dragon_hall.west = self.princess_cell
        self.dragon_hall.east = self.choice_3

        self.princess_cell.east = self.choice_3

        # Set up other
        self.loc = self.dungeon_cell
        self.inventory = []
        self.equipment = [None,
                          self.ruined_shirt,
                          self.ruined_shorts,
                          None,
                          None]
        self.deadliness = 0

    # Equipment is
    # [Head, Chest, Legs, Feet, Hand]

    def carrying(self):
        out_str = "You are carrying: "
        for item in self.inventory:
            out_str = out_str + item.description
            if self.inventory[-1] == item:
                out_str = out_str + '.'
            else:
                out_str = out_str + ', '
        if len(self.inventory) == 0:
            print("You are carrying nothing.")
        else: print(out_str)

    def equipped(self):
        out_str = "You are wearing: "
        copy_equip = []
        for item in self.equipment:
            if str(item) != 'None':
                copy_equip.append(item)
        for item in copy_equip:
            out_str = out_str + item.description
            if self.equipment[-1] == item:
                out_str = out_str + '.'
            else:
                out_str = out_str + ', '
        if len(copy_equip) == 0:
            print("You currently have nothing equipped.")
        else:
            print(out_str)

    def equip(self, descr):
        for item in self.inventory:
            if descr in item.description:
                print()

    def lookaround(self) -> str:
        out_str = "You see: "
        combo_list = self.loc.items + self.loc.creatures
        for item in combo_list:
            out_str = out_str + item.description
            if combo_list[-1] == item:
                out_str = out_str + '.'
            else:
                out_str = out_str + ', '
        if len(combo_list) == 0:
            return "You don't see anything."
        return out_str

    def examine(self, descr: str):
        found = False
        for item in self.inventory:
            if descr in item.description:
                print(item.extDescription)
                found = True
        for item in self.loc.items:
            if descr in item.description:
                print(item.extDescription)
                found = True
                if 'well' in item.description and self.loc == self.well_of_beasts:
                    self.death('beast well')
        for creature in self.loc.creatures:
            if descr in creature.description:
                print(creature.extDescription)
                found = True
        if found == False:
            print("There is no '" + descr + "' here.")

    def take(self, descr: str):
        pickedup = False
        for item in self.loc.items:
            if descr in item.description:
                if item.movable == True:
                    self.inventory.append(item)
                    self.loc.items.remove(item)
                    print("You picked up " + str(item.description) + ". ")
                    self.carrying()
                    pickedup = True
                else:
                    print("You can't take that!")
                    pickedup = True
        for creature in self.loc.creatures:
            if descr in creature.description:
                print("You can't pick up " + descr + '.')
                pickedup = True
        if pickedup != True:
            print("There is no " + descr + " here.")

    def drop(self, descr: str):
        doprint = True
        for item in self.inventory:
            if descr in item.description:
                print("You drop " + item.description + ". ")
                self.loc.items.append(item)
                self.inventory.remove(item)
                self.carrying()
                doprint = False
                break
        if doprint: print("You are not carrying " + descr + ".")

    def look(self):
        out = ''
        out += f"You are {self.loc.description}."
        for feature in self.loc.features:
            out += '\n' + str(feature)
        return out

    def go(self, dir: str):
        northlocked = False
        southlocked = False
        eastlocked = False
        westlocked = False
        uplocked = False
        downlocked = False
        if self.loc == self.dungeon_cell and self.cell_key not in self.inventory:
            southlocked = True
        elif self.loc == self.dragon_hall and self.dragon_heart not in self.inventory:
            westlocked = True
        elif self.loc == self.dragon_hall and self.dragon_heart in self.inventory:
            self.loc.features = []
        if dir in ['North', 'north', 'N', 'n']:
            if self.loc.north is not None and not northlocked:
                self.loc = self.loc.north
                print(self.look())
            elif self.loc.north is not None and northlocked:
                print('That exit is locked.')
            else:
                print("You can't go that way.")
        elif dir in ['South', 'south', 'S', 's']:
            if self.loc.south is not None and not southlocked:
                self.loc = self.loc.south
                print(self.look())
            elif self.loc.south is not None and southlocked:
                print('That exit is locked.')
            else:
                print("You can't go that way.")
        elif dir in ['East', 'east', 'E', 'e']:
            if self.loc.east is not None and not eastlocked:
                self.loc = self.loc.east
                print(self.look())
            elif self.loc.east is not None and eastlocked:
                print('That exit is locked.')
            else:
                print("You can't go that way.")
        elif dir in ['West', 'west', 'W', 'w']:
            if self.loc.west is not None and not westlocked:
                self.loc = self.loc.west
                print(self.look())
            elif self.loc.west is not None and westlocked:
                print('That exit is locked.')
            else:
                print("You can't go that way.")
        elif dir in ['Up', 'up', 'U', 'u', '^']:
            if self.loc.up is not None and not uplocked:
                self.loc = self.loc.up
                print(self.look())
            elif self.loc.up is not None and uplocked:
                print('That exit is locked.')
            else:
                print("You can't go that way.")
        elif dir in ['Down', 'down', 'D', 'd', 'v']:
            if self.loc.down is not None and not downlocked:
                self.loc = self.loc.down
                print(self.look())
            elif self.loc.down is not None and downlocked:
                print('That exit is locked.')
            else:
                print("You can't go that way.")
        if self.loc in [self.hall_of_guards, self.falldeath, self.mimic_room]:
            if self.loc == self.mimic_room:
                print("It was a monster that looks like a chest- a mimic!")
            else:
                print("It's a trap!")
            self.death('trap')
        elif self.loc == self.end:
            self.victory()

    def kill(self, descr: str) -> str:
        creature_found = False
        if self.hero_sword in self.inventory:
            self.deadliness = 3
        elif self.guard_sword in self.inventory:
            self.deadliness = 2

        for creature in self.loc.creatures:
            if creature.killable == True and creature.deadliness <= self.deadliness:
                print('You kill ' + creature.description + '.')
                self.inventory.append(creature.reward)
                print('It dropped ' + creature.reward.description + '!')
                self.loc.creatures.remove(creature)
                creature_found = True
            elif creature.killable == False and creature.deadliness <= self.deadliness:
                print(creature.desc + ' cannot be killed.')
                creature_found = True
            elif creature.killable == False and creature.deadliness >= self.deadliness:
                print('You failed to kill ' + creature.desc + '.')
                print('It attacks you!')
                self.death('creature')
            elif creature.killable == True and creature.deadliness >= self.deadliness:
                print("You aren't strong enough to kill " + creature.description + '!')
                print('It attacks you!')
                self.death('creature')
        if creature_found == False:
            print('There is no ' + descr + ' here.')

    def death(self, deathtype: str):
        if deathtype == 'creature':
            print('You are viciously slain!')
        elif deathtype == 'self':
            print('You got yourself killed...')
        elif deathtype == 'trap':
            print('You have died a horrible death.')
        elif deathtype == 'beast well':
            print('As you drink the water, your vision blurs... \n')
            print('You slowly transform into a mindless beast, cursed to wander the castle until you die.')
        elif deathtype == 'random':
            print('Wow, you died. That stinks.')
        elif deathtype == 'null':
            print('You have died.')
        else:
            print('You died in a very mysterious way. Congrats.')
        print('Thanks for playing... try again if you dare.')
        input('(Press Enter to Close)')
        exit()

    def victory(self):
        print('Congratulations, you escaped the castle!')
        out_str = 'Completion: '
        if self.princess not in self.inventory and self.hero_sword not in self.inventory and self.loc == self.end:
            out_str = out_str + '33%'
        elif self.princess not in self.inventory and self.hero_sword in self.inventory:
            out_str = out_str + '66%'
        elif self.princess in self.inventory:
            out_str = out_str + '*100%*'
        elif self.loc != self.end:
            out_str = out_str + '0%'
            print('You dirty, dirty cheater.')
        exit(out_str)


world = World()


class Game(cmd.Cmd):
    prompt = '\n>>'
    intro = world.look()

    def do_go(self, arg):
        """Move in a cardinal direction\nUsage: go <direction>\nDirections: [N, S, E, W, Up, Down]"""
        world.go(arg)

    def do_kill(self, arg):
        """Attempt to kill a creature in the room\nUsage: kill <description>\nDescription: Text description of enemy / creature"""
        world.kill(arg)

    def do_look(self, arg):
        """Get a general room description\nUsage: look"""
        print(world.look())

    def do_lookaround(self, arg):
        """Get a list of everything inside a room\nUsage: lookaround"""
        print(world.lookaround())

    def do_drop(self, arg):
        """Attempt to drop an item\nUsage: drop <description>\nDescription: Text description of item"""
        world.drop(arg)

    def do_take(self, arg):
        """Attempt to take an item\nUsage: take <description>\nDescription: Text description of item"""
        world.take(arg)

    def do_examine(self, arg):
        """Get a closer look at an object\nUsage: examine <description>\nDescription: Text description of object"""
        world.examine(arg)

    def do_equip(self, arg):
        """Equip a piece of equipment from your inventory\nUsage: equip <description>\nDescription: Text description of equipment in inventory"""
        world.equip(arg)

    def do_equipped(self, arg):
        """Check what gear you have equipped\nUsage: equipped"""
        world.equipped()

    def do_carrying(self, arg):
        """Check your inventory\nUsage: carrying"""
        world.carrying()

    def do_exit(self, arg):
        """Close the game\nUsage: exit"""
        exit()

    def do_quit(self, arg):
        """Runs exit"""
        self.do_exit(arg)

    def postcmd(self, stop: bool, line: str) -> bool:
        world.look()
        return False


game = Game()
game.cmdloop()
