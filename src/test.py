import unittest
from main_parse import get_median_sum,valid_date

class TestValidDate(unittest.TestCase):
	
	def test_true_date(self):
		self.assertTrue(valid_date("12312016"))
		self.assertTrue(valid_date("01312016"))
		self.assertTrue(valid_date("02292016"))
		self.assertTrue(valid_date("02292016"))
		self.assertTrue(valid_date("02281991"))
		self.assertTrue(valid_date("05302016"))
		self.assertTrue(valid_date("05301991"))

	def test_false_date(self):
		self.assertFalse(valid_date("02312016"))
		self.assertFalse(valid_date("02302016"))
		self.assertFalse(valid_date("02002016"))
		self.assertFalse(valid_date("00292016"))
		self.assertFalse(valid_date("02292017"))
		self.assertFalse(valid_date("06312017"))
		self.assertFalse(valid_date("02291900"))
		
	def test_median(self):
<<<<<<< HEAD
		
=======
		self.assertEqual(get_median_sum({},"x","y",1),(1,1,1))
>>>>>>> 96f50a4ba5247a7382dd52d6af5831e047fcc6bf
		D={}
		for num,expect in zip([1,6,5,2,4,3],[1,4,5,4,4,4]):
			median,total,count = get_median_sum(D,"x","y",num)
			self.assertEqual(median,expect)
		D={}
		for num,expect in zip([23,12,9,11,50],[23,18,12,12,12]):
			median,total,count = get_median_sum(D,"x","y",num)
			self.assertEqual(median,expect)
		
		D={}
		for num,expect in zip([15,12,10,8,7,6],[15,14,12,11,10,9]):
			median,total,count = get_median_sum(D,"x","y",num)
			self.assertEqual(median,expect)		
		
		
	
	


if __name__ == "__main__":
	unittest.main()