from main import *
import unittest

class TestBotMethods(unittest.TestCase):
	def test_is_nut(self):
		self.assertTrue(is_nut('Almond'))
		self.assertTrue(is_nut('Hazelnut'))
		self.assertFalse(is_nut(''))
	def test_get_flavor_amount(self):
		self.assertTrue(get_flavor_amount('Lavender') == '3 tbsp')
		self.assertTrue(get_flavor_amount('Nutmeg') in ['1/2 tsp', '1/4 tsp'])
		self.assertFalse(get_flavor_amount('Vanilla') == '3 tbsp')
		self.assertTrue(get_flavor_amount('') == "get_flavor_amount wrong input")
	def test_get_spices(self):
		self.assertTrue(len(get_spices(3)) == 3)
		self.assertTrue(get_spices(1) in [['Cinnamon'], ['Cardamom']])
	def test_get_extracts(self):
		self.assertFalse('Vanilla' in get_extracts(0))
		self.assertTrue('Vanilla' in get_extracts(3))
	def test_zest_extract_same(self):
		self.assertFalse(zest_extract_same_flavor('Lemon Extract','Hazelnut'))
		self.assertFalse(zest_extract_same_flavor('Lemon Extract',''))
		self.assertFalse(zest_extract_same_flavor('Lemon Extract','1 2 3'))
		self.assertTrue(zest_extract_same_flavor('Lemon Extract','Lemon Zest'))
		self.assertFalse(zest_extract_same_flavor('Lemon Extract','Anything Zest'))
	def test_get_fruit_purees(self):
		self.assertTrue(len(get_fruit_purees()) <= 2)
	def test_get_fruit_purees_percent(self):
		self.assertTrue(len(get_fruit_purees_percent(['Banana','Apple']))==2)
		self.assertTrue(len(get_fruit_purees_percent(['Apple']))==1)
		self.assertTrue(get_fruit_purees_percent([])==[0])
		self.assertTrue(sum(get_fruit_purees_percent(['Banana','Apple']))<=50)
		self.assertTrue(sum(get_fruit_purees_percent(['Banana','Apple']))>=25)
	def test_sandwich(self):
		self.assertTrue(sandwich(None, 10000) == None)

if __name__ == '__main__':
	unittest.main()
