import unittest
from finalproject import *

#matthew wolfgram
#si 206 003

class testcollection(unittest.TestCase):

    def test_collection(self):
        test0 = process_command('bar ram')
        self.assertGreater(len(test0), 0) #ensures the user command is processed correctly
        self.assertEqual(test0[-1][-1], .2) #ensures relevant data is returned from process_command based on the user command

        test1 = process_command('scatter battery brand')
        self.assertGreater(len(test0), 0) #ensures the user command is processed correctly
        self.assertEqual(test1[-1][-1], 1300) #ensures relevant data is returned from process_command based on the user command
        self.assertEqual(test1[-1][0], 'fusion garage') #ensures the process_command function correctly populates information per brand

class testfetch(unittest.TestCase):

    def test_fetch(self):
        test2 = fetch_data('apple')
        self.assertGreater(len(test2), 0) #ensures the fetch_data function accumulates data properly for the brand 'apple'
        self.assertTrue('apple' in test2.keys()) #ensures phoenarena information for the brand 'apple' is gotten from the fetch_data function

        test3 = fetch_data('samsung')
        self.assertGreater(len(test3), 0) #ensures the fetch_data function accumulates data properly for the brand 'samsung'
        self.assertTrue('samsung' in test3.keys()) #ensures phonearena information for the brand 'samsung' is gotten from the fetch_data function

        test4 = fetch_data('motorola')
        self.assertGreater(len(test4), 0) #ensures the fetch_data function accumulates data properly for the brand 'motorola'
        self.assertTrue('motorola' in test4.keys()) #ensures phonearena information for the brand 'motorola' is gotten from the fetch_data function

class testdatabase(unittest.TestCase):

    def test_database(self):
        conn = sqlite3.connect('mobile.db')
        cur = conn.cursor()

        sql = '''
            SELECT mobiledata.brand, AVG(`ram size (gb)`)
                FROM mobiledata
                JOIN `foreign keys` as f
                ON mobiledata.brandId = f.Id
                GROUP BY mobiledata.brand
                ORDER BY AVG(`ram size (gb)`) DESC
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn('razer', result_list[0][0])#ensures brand 'razer' is the first brand in the result_list
        self.assertIn('niu', result_list[-1][0]) #ensures brand 'niu' is the last brand in the result_list
        self.assertEqual(len(result_list[3]), 2) #ensures the specific sql command returns a tuple of length 2
        self.assertGreater(len(result_list), 60) #ensures the specific sql command returns results, and also that the foreign keys are constructed properly

        sql = '''
            SELECT COUNT(*)
            FROM mobiledata
        '''
        results = cur.execute(sql)
        count = results.fetchone()[0]
        self.assertGreater(count, 900) #ensures database was correctly populated

        conn.close()

unittest.main()
