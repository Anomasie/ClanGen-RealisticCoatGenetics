import random
from random import choice

import json

class PeltGenome:
    # base color series
    pelt_colours_black_series = [
        "BLACK",    # BLACK
        "GHOST",    # BLACK + smoked
        "SILVER",   # BLACK + shaded
        "DARKGREY", # BLACK + dd
        "GREY",     # BLACK + dd + smoked
        "PALEGREY", # BLACK + dd + shaded
        "LILAC",    # BLACK + dd + caramel
        "LILAC",    # BLACK + dd + caramel + smoked
        "LIGHTBROWN",    # BLACK + dd + caramel + shaded
    ]
    pelt_colours_brown_series = [
        "CHOCOLATE",    # BROWN
        "DARKBROWN",    # BROWN + smoked
        "LILAC",        # BROWN # shaded
        "GOLDEN-BROWN", # BROWN + dd
        "PALEGINGER",   # BROWN + dd + smoked
        "CREAM",        # BROWN + dd + shaded
        "LILAC",        # BROWN + dd + caramel
        "LILAC",        # BROWN + dd + caramel + smoked
        "LIGHTBROWN",   # BROWN + dd + caramel + shaded
    ]
    pelt_colours_cinnamon_series = [
        "SIENNA",       # CINNAMON
        "SIENNA",       # CINNAMON + smoked
        "PALEGINGER",   # CINNAMON + shaded
        "GREY",         # CINNAMON + dd
        "SILVER",       # CINNAMON + dd + smoked
        "PALEGREY",     # CINNAMON + dd + shaded
        "LIGHTBROWN",   # CINNAMON + dd + caramel
        "LIGHTBROWN",   # CINNAMON + dd + caramel + smoked
        "WHITE",        # CINNAMON + dd + caramel + shaded
    ]
    pelt_colours_red_series = [
        "DARKGINGER",   # RED
        "GINGER",       # RED + smoked
        "CREAM",        # RED + shaded
        "PALEGINGER",   # RED + dd
        "PALEGINGER",   # RED + dd + smoked
        "CREAM",        # RED + dd + shaded
        "GOLDEN",       # RED + dd + caramel
        "GOLDEN",       # RED + dd + caramel + smoked
        "CREAM",        # RED + dd + caramel + shaded
    ]

    # patterns
    ## Missing: SingleColour, TwoColour, Smoke, Tortie, Calico
    pelt_patterns_blotched = [
        "Tabby",
        "Classic",
        "Sokoke",
        "Marbled"
    ]
    pelt_patterns_mackerel = [
        "Mackerel",
        "Masked"
    ]
    pelt_patterns_spotted = [
        "Speckled",
        "Rosette",
        "Bengal"
    ]
    pelt_patterns_ticked = [
        "Ticked",
        "Agouti",
        "Singlestripe"
    ]
    pelt_patterns_no_stripes = [
        "SingleColour",
        "TwoColour",
        "Smoke"
    ]

    # load json files
    with open('resources/genetics/pelt_genotypes.json') as f:
        pelt_genotypes = json.load(f)
    with open('resources/genetics/pelt_phenotypes.json') as f:
        pelt_phenotypes = json.load(f)
    with open('resources/genetics/pelt_genotypes_requirements.json') as f:
        pelt_genotype_requirements = json.load(f)
    
    def __init__(
        self,
        genotype: dict = None,
        phenotype: dict = None,
        pelt = None,
        sex = None,
        permanent_conditions = {}
    ) -> None:
        if genotype:
            self.genotype = genotype
            self.phenotype = self.get_phenotype_from_genotype()
        elif phenotype:
            self.genotype = self.get_genotype_from_phenotype(phenotype)
            self.phenotype = phenotype
        elif pelt:
            self.init_from_pelt(pelt, sex, permanent_conditions)
        else:
            self.randomize(sex)
            if "deaf" in permanent_conditions:
                self.phenotype["hearing"] = ["deaf"]
        
    def init_from_pelt(self, pelt, sex, permanent_conditions = {}):
        self.phenotype = self.get_phenotype_from_pelt(pelt, sex, permanent_conditions)
        self.genotype = self.get_genotype_from_phenotype(self.phenotype)
    
    # ------------------------------------------------------------------------------------------------------------#
    #   RANDOM GENOME GENERATION
    # ------------------------------------------------------------------------------------------------------------#

    def randomize(self, sex = None) -> None:
        self.random_genotype(female=(sex=="female"))
        self.phenotype = self.get_phenotype_from_genotype()

    def random_genotype(self, female = None) -> None:
        # random dna
        self.genotype = {}
        for chromosome in self.pelt_genotypes.keys():
            self.genotype[chromosome] = [
                self.random_trait(self.pelt_genotypes[chromosome]),
                self.random_trait(self.pelt_genotypes[chromosome])
            ]
            self.genotype[chromosome].sort()
        if female is None:
            female = choice([True, False])
        if not female: # delete second X-chromosome
            self.genotype["X"] = [self.genotype["X"][0]]

    def random_trait(self, options) -> str:
        given_trait = ""
        random_number = random.randint(1, 100)
        summe = 0
        for option in options.keys():
            summe += options[option]["rarity"]
            if given_trait == "" and random_number <= summe:
                given_trait = options[option]["gen"]
        return given_trait

    def get_allel_combination_probability(self, chromosome_key, comb) -> float:
        chromosome = self.pelt_genotypes[chromosome_key]
        # are all entries valid?
        for allel in comb:
            if not allel in chromosome:
                return 0
        # edge cases: len(comb) != 2
        if len(comb) == 0:
            return 0
        if len(comb) == 1:
            return chromosome[comb[0]]["rarity"] / 100
        if len(comb) > 2:
            return 0
        # general case: comb consists of two allels
        if comb[0] != comb[1]:
            return (chromosome[comb[0]]["rarity"] / 100) * (chromosome[comb[1]]["rarity"] / 100) * 2
        else:
            return (chromosome[comb[0]]["rarity"] / 100) * (chromosome[comb[1]]["rarity"] / 100)

    # ------------------------------------------------------------------------------------------------------------#
    #   REALISTIC INHERITANCE
    # ------------------------------------------------------------------------------------------------------------#

    def from_parents( self, parent_1, parent_2, sex=None):
        # generate kitten_dna
        self.genotype = {}
        # go through every chromosome
        for chromosome in parent_1.genotype.keys():
            self.genotype[chromosome] = [choice(parent_1.genotype[chromosome]), choice(parent_2.genotype[chromosome])]
            self.genotype[chromosome].sort()
        # sex: male kittens get their X chromosome from their mother
        if sex == "male" or (sex is None and random.random() < 0.5): # male kitten
            if parent_1.is_female():
                self.genotype["X"] = [choice(parent_1.genotype["X"])]
            else: # if both parents are male, then the kitten gets the second parent's X-chromosome
                self.genotype["X"] = [choice(parent_2.genotype["X"])]
        # set other variables
        self.phenotype = self.get_phenotype_from_genotype()

    # ------------------------------------------------------------------------------------------------------------#
    #   GENOTYPE <-> PHENOTYPE <-> PELT
    # ------------------------------------------------------------------------------------------------------------#

    # genotype -> phenotype

    def has_trait(self, trait, genotype) -> bool:
        if "require" in trait.keys():
            for condition in trait["require"]:
                # size requirements
                if "size" in condition.keys():
                    if len(genotype[condition["locus"]]) != condition["size"]:
                        return False
                # allel requirements
                if "gen" in condition.keys():
                    # specific allels required
                    if type(condition["gen"]) is list:
                        if genotype[condition["locus"]] != condition["gen"]:
                            return False
                    else:
                        if not condition["gen"] in genotype[condition["locus"]]:
                            return False
        return True
    
    def get_phenotype_from_genotype(self, genotype=None) -> dict:
        if genotype is None: genotype = self.genotype
        if not self.check_genotype(genotype):
            print("WARNING in pelt_genome.py, get_phenotype_from_genotype: the following genotype is not valid.")
            print(genotype)

        phenotype = {}
        for feature in self.pelt_phenotypes.keys(): # such as diluted, color, ...
            result = []
            found = False
            exclusive_mode = True
            # go through every possible option
            for option in self.pelt_phenotypes[feature]:
                if not found:
                    if "exclusive" in option.keys():
                        # case 1: option needs to stand alone
                        if option["exclusive"] and exclusive_mode:
                            if self.has_trait(option, genotype):
                                result.append(option["trait"])
                                found = True
                        # case 2: one other trait can be appended after this one
                        elif not option["exclusive"]:
                            if self.has_trait(option, genotype):
                                result.append(option["trait"])
                                exclusive_mode = False
                    else:
                        if self.has_trait(option, genotype):
                            result.append(option["trait"])
                            found = True # finish searching
            phenotype[feature] = result
        return phenotype
    
    # pelt -> phenotype

    def has_feature(self, phenotype, feature) -> bool:
        # no requirements
        if not "require" in feature:
            return True
        # check requirements
        for requirement in feature["require"]:
            if "feature" in requirement and not requirement["feature"] in phenotype[requirement["category"]]:
                return False
            if "feature_in" in requirement:
                found_one = False
                for has_features in phenotype[requirement["category"]]:
                    if has_features in requirement["feature_in"]:
                        found_one = True
                if not found_one:
                    return False
            if "size" in requirement and not len(phenotype[requirement["category"]]) == requirement["size"]:
                return False
        return True

    def get_phenotype_from_pelt(self, pelt, sex, permanent_conditions = {}) -> dict:
        phenotype = {}

        # eyes
        all_eye_colors = [pelt.blue_eyes, pelt.green_eyes, pelt.yellow_eyes, ["COPPER"], ["BRONZE", "AMBER", "HAZEL"]]
        possibilities = []
        for i in range(len(all_eye_colors)):
            if pelt.eye_colour in all_eye_colors[i]:
                possibilities.append(i)
        i = 0
        if len(possibilities) > 0:
            i = choice(possibilities)
        phenotype["eyes"] = [["blue", "green", "yellow", "red", "brown"][i]]

        if pelt.eye_colour2:
            phenotype["eyes"].append("blue")

        # hearing
        if "deaf" in permanent_conditions:
            phenotype["hearing"] = ["deaf"]
        else:
            phenotype["hearing"] = ["hearing"]

        # length
        phenotype["length"] = [pelt.length]

         # stripes
        phenotype["stripes"] = ["no stripes"]
        all_stripe_series = [self.pelt_patterns_mackerel, self.pelt_patterns_blotched, self.pelt_patterns_spotted, self.pelt_patterns_ticked]
        possibilities = []
        for i in range(len(all_stripe_series)):
            if pelt.name in all_stripe_series[i]:
                possibilities.append(i)
        if len(possibilities) > 0:
            phenotype["stripes"] = [["mackerel", "blotched", "spotted", "ticked"][choice(possibilities)]]

        # color & diluted & hair tips
        ## get possible base colors
        all_series = [self.pelt_colours_black_series, self.pelt_colours_brown_series, self.pelt_colours_cinnamon_series, self.pelt_colours_red_series, ["WHITE"]]
        possibilities = []
        for i in range(len(all_series)):
            if pelt.colour in all_series[i]:
                possibilities.append(i)
        i = 4
        ### red cats always have stripes => if stripes, then prefer non-red color
        if phenotype["stripes"] == ["no stripes"]:
            if 3 in possibilities and possibilities != [3]:
                possibilities.remove(3)
            else:
                phenotype["color"] = ["red"]
                phenotype["stripes"].append("light")
        ### white cats don't have stripes, spots, pointer
        if pelt.colour == "WHITE" and pelt.name in ["SingleColour", "TwoColour"] and pelt.white_patches is None and pelt.points is None:
            possibilities = [4]
        elif 4 in possibilities: 
            possibilities.remove(4)
        ## choose base color
        if len(possibilities) > 0:
            i = choice(possibilities)
        phenotype["color"] = [["black", "brown", "cinnamon", "red", "white"][i]]
        ### find position in series
        possibilities = [k for k, x in enumerate(all_series[i]) if x == pelt.colour]
        if len(possibilities) > 0:
            j = choice(possibilities)
            phenotype["diluted"] = [["full-color", "diluted", "caramelized"][int(j/3)]]
            phenotype["hair tips"] = [["full-color", "smoked", "shaded"][j % 3]]
        else:
            phenotype["diluted"] = [choice(["full-color", "diluted", "caramelized"])]
            if random.random() > self.get_allel_combination_probability("D2", ["i", "i"]): # smoked/shaded or full-color?
                # no stripes -> smoked
                if pelt.name in ["SingleColour", "TwoColour"]:
                    phenotype["hair tips"] = ["smoked"]
                else: # stripes -> shaded
                    phenotype["hair tips"] = ["shaded"]
            else:
                phenotype["hair tips"] = ["full-color"]

        # pointer
        if pelt.points is None:
            phenotype["pointer"] = ["full-color"]
        elif pelt.points in ["SEALPOINT", "MINKPOINT"]:
            phenotype["pointer"] = ["mink"]
        elif pelt.points == "COLOURPOINT":
            phenotype["pointer"] = ["burma"]
        elif pelt.points == "RAGDOLL":
            phenotype["pointer"] = ["siam"]
        else:
            phenotype["pointer"] = ["full-color"]
            if phenotype["hair tips"][0] == "full_color": # pelt.points = SEPIAPOINT -> cat should be smoked or shaded
                if pelt.name in ["SingleColour", "TwoColour"]:
                    phenotype["hair tips"] = ["smoked"]
                else:
                    phenotype["hair tips"] = ["shaded"]

        # sex
        phenotype["sex"] = [sex]

        # spots
        if pelt.white_patches is None:
            phenotype["spots"] = ["full-color"]
        elif pelt.white_patches in pelt.tuxedo_white and pelt.vitiligo in ["VITILIGO", "VITILIGOTWO"]:
            phenotype["spots"] = ["salty licorice"]
        else:
            all_spot_possibilities = [pelt.little_white, pelt.mid_white, pelt.high_white, pelt.mostly_white, pelt.paws_white]
            possibilities = []
            for i in range(len(all_spot_possibilities)):
                if pelt.eye_colour in all_eye_colors[i]:
                    possibilities.append(i)
            i = 0
            if len(possibilities) > 0:
                i = choice(possibilities)
            phenotype["spots"] = [["small white spots", "small white spots", "big white spots", "big white spots", "gloves"][i]]
        
        # vitiligo
        phenotype["vitiligo"] = ["full-color"]
        if not pelt.vitiligo is None and (phenotype["spots"] != ["salty licorice"] or random.random() < 0.1):
            phenotype["vitiligo"] = ["vitiligo"]

        return phenotype

    # phenotype -> genotype

    def get_genotype_from_phenotype(self, phenotype) -> dict:
        genotype = {}
        for locus in self.pelt_genotype_requirements.keys():
            result = []
            i = 0
            # go through every possible option
            for option in self.pelt_genotype_requirements[locus]:
                if len(result) == 0 and self.has_feature(phenotype, option):
                    if "trait" in option.keys():
                        result = option["trait"]
                    elif "traits" in option.keys():
                        # get distribution
                        distribution = []
                        for poss in option["traits"]:
                            distribution.append(self.get_allel_combination_probability(locus, poss))
                        result = random.choices(option["traits"], weights=distribution)[0]
                    else:
                        result = [
                            self.random_trait(self.pelt_genotypes[locus]),
                            self.random_trait(self.pelt_genotypes[locus])
                        ]
                i += 1
            if len(result) == 0:
                result = [
                    self.random_trait(self.pelt_genotypes[locus]),
                    self.random_trait(self.pelt_genotypes[locus])
                ]
            genotype[locus] = result
        return genotype

    # pelt -> genotype

    def get_genotype_from_pelt(self, pelt, sex, permanent_condition={}) -> dict:
        return self.get_genotype_from_phenotype(
            self.get_phenotype_from_pelt(
                pelt,
                sex,
                permanent_condition
            )
        )
    
    # help functions

    def check_genotype(self, genotype=None) -> bool:
        if genotype is None: genotype = self.genotype
        # check dna
        if not genotype:
            print("WARNING in check_genotype: no genotype")
            return False
        for locus in self.pelt_genotypes.keys():
            if locus in genotype.keys():
                # enough allels?
                if len(genotype[locus]) > 2:
                    print("WARNING in check_genotype: too many allels at locus ", locus)
                    return False # too many allels
                elif len(genotype[locus]) == 1 and locus != "X":
                    print("WARNING in check_genotype: too few allels at locus ", locus)
                    return True # too few allels
                elif len(genotype[locus]) == 0 and locus == "X":
                    print("WARNING in check_genotype: too few allels at locus ", locus)
                    return False # too few allels
    			# does this allel exist?
                for allel in genotype[locus]:
                    if not allel in self.pelt_genotypes[locus]:
                        print("WARNING in check_genotype: allel ", allel, " not known at locus ", locus)
                        return False
            # chromosome missing => damaged dna
            else:
                print("WARNING in check_genotype: missing allel")
                return False
        return True
    
    def is_female(self) -> bool:
        if self.check_genotype():
            return len(self.genotype["X"]) == 2
        else:
            print("ERROR in is_female: invalid dna")
