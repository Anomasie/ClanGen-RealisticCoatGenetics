<!-- Write BELOW The Headers and ABOVE The comments else it may not be viewable. -->
<!-- You can view CONTRIBUTING.md for a detailed description of the pull request process. -->
<!-- Be sure to name your PR something descriptive and succinct; include Bugfix: Feature: Enhancement: or Content: in the title to describe what type of PR it is. -->
<!-- IF YOU ARE DOING A BUGFIX: Please target the latest release branch if the bug that you are fixing is also present in the latest release. -->

## About The Pull Request

<!-- Describe The Pull Request. Please be sure every change is documented or this can delay review and even discourage senior developers from merging your PR! -->

The goal is to add the option of realistic pelt inheritance to the game. If this version is started, a new option appears in *relation settings*: *realistic pelt behavior*. Each cat gets their own dna attached, which is initially calculated from their pelt. If *realistic pelt behavior* is checked, the following happens:

- New cats will first generate their dna and construct their pelt color using that.
- This results in a different pelt color distribution.
- Thus, unrealistic pelt colors (for example, red without stripes) will not be generated anymore.
- When a kitten is born, its pelt will be calculated on base on its dna, which is inherited from its parents.
- This also works for same-sex-pairs, if *same sex pregnancy* is allowed.

If the option is not selected, the game behaves as usual. Old cats will *not* change their pelts if this option is checked.

## Why This Is Good For ClanGen

I think it is fun to learn about genetics.

## Proof of Testing

Below there are genotype (dna) and phenotype (dict which describes the appearance) of both parents and their 4 kittens, printed out.

Parent 1:

		pelt_genome.genotype = {
			'A1': ['Ti+', 'Ti+'], 'A3': ['a', 'a'], 'B1': ['TaM', 'Tab'],
			'BS': ['sp', 'sp'], 'C1': ['D', 'd'], 'CAR': ['dm', 'dm'],
			'CURL': ['R', 'r'], 'D1': ['C', 'C'], 'D2': ['I', 'i'],
			'D4': ['B', 'b'], 'EYE': ['more', 'more'], 'KIT': ['w', 'w'],
			'LEN': ['L', 'L'], 'ODD_EYE': ['homo', 'homo'],
			'VIT': ['V', 'v'], 'X': ['O', 'O']
		}
		pelt_genome.phenotype = {
			'eyes': ['brown'], 'hearing': ['hearing'], 'length': ['short'],
			'stripes': ['no stripes', 'light'], 'color': ['red'],
			'diluted': ['full-color'], 'hair tips': ['smoked'],
			'pointer': ['full-color'], 'sex': ['female'],
			'spots': ['full-color'], 'vitiligo': ['full-color']
		}

Parent 2:

		pelt_genome.genotype = {
			'A1': ['Ti+', 'Ti+'], 'A3': ['A', 'a'], 'B1': ['Tab', 'Tab'],
			'BS': ['Sp', 'sp'], 'C1': ['D', 'D'], 'CAR': ['Dm', 'Dm'],
			'CURL': ['R', 'r'], 'D1': ['C', 'C'], 'D2': ['i', 'i'],
			'D4': ['B', 'b'], 'EYE': ['more', 'mid'], 'KIT': ['wg', 'w'],
			'LEN': ['L', 'l'], 'ODD_EYE': ['homo', 'homo'],
			'VIT': ['V', 'v'], 'X': ['o']
		}
		pelt_genome.phenotype = {
			'color': ['black'], 'diluted': ['full-color'],
			'eyes': ['yellow'], 'hair tips': ['full-color'],
			'hearing': ['hearing'], 'length': ['short'],
			'pointer': ['full-color'], 'sex': ['male'],
			'spots': ['full-color'], 'stripes': ['spotted'],
			'vitiligo': ['full-color']
		}

A possible kitten:
		
		pelt_genome.genotype = {
			'A1': ['Ti+', 'Ti+'], 'A3': ['A', 'a'], 'B1': ['TaM', 'Tab'],
			'BS': ['Sp', 'sp'], 'C1': ['D', 'd'], 'CAR': ['Dm', 'Dm'],
			'CURL': ['R', 'r'], 'D1': ['C', 'C'], 'D2': ['i', 'i'],
			'D4': ['B', 'b'], 'EYE': ['more', 'less'], 'KIT': ['wg', 'w'],
			'LEN': ['L', 'L'], 'ODD_EYE': ['homo', 'homo'],
			'VIT': ['V', 'v'], 'X': ['O']
		}
		pelt_genome.genotype = {
			'eyes': ['green'], 'hearing': ['hearing'], 'length': ['short'],
			'stripes': ['spotted'], 'color': ['red'],
			'diluted': ['full-color'], 'hair tips': ['full-color'],
			'pointer': ['full-color'], 'sex': ['male'],
			'spots': ['full-color'], 'vitiligo': ['full-color']
		}

Here are pictures of the parents and their 4 kittens.

[Two parents, a female ginger cat and a male black one, with their four kittens. Male kittens are all red and female kittens are all torties.](clangen-realistic-pelt-example.png)

## Changelog/Credits

If you want to credit the websites I got my information from, here they are:

- http://messybeast.com/colour-charts.htm
- https://en.wikipedia.org/wiki/Cat_coat_genetics
- https://www.jstor.org/stable/24953922 (as an orientation for the allel distribution)