import unittest
import pokemon

class PokemonTestCase(unittest.TestCase):
    
    def setUp(self):
        self.charmander = pokemon.Firetype("Charmander", 1)
        self.squirtle = pokemon.Watertype("Squirtle", 2)

    def test_startingHealth(self):
        self.assertEqual(
            self.charmander.starting_health,
            1900
        )
        self.assertEqual(
            self.squirtle.starting_health,
            2200
        )

if __name__ == "__main__":
    unittest.main()