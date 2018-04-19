import unittest
from finalproject import *


class testcollection(unittest.TestCase):

    def test_collection(self):
        test0 = process_command('bar ram')
        self.assertGreater(len(test0), 0)
        self.assertEqual(test0[-1][-1], .2)

        test1 = process_command('scatter battery brand')
        self.assertGreater(len(test0), 0)
        self.assertEqual(test1[-1][-1], 1300)
        self.assertEqual(test1[-1][0], 'fusion garage')

class testfetch(unittest.TestCase):

    def test_fetch(self):
        test2 = fetch_data('apple')
        self.assertGreater(len(test2), 0)
        self.assertTrue('apple' in test2.keys())

        test3 = fetch_data('samsung')
        self.assertGreater(len(test3), 0)
        self.assertTrue('samsung' in test3.keys())

        test4 = fetch_data('motorola')
        self.assertGreater(len(test4), 0)
        self.assertTrue('motorola' in test4.keys())

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
        self.assertIn('razer', result_list[0][0])
        self.assertIn('niu', result_list[-1][0])
        self.assertGreater(len(result_list), 60)

        sql = '''
            SELECT COUNT(*)
            FROM mobiledata
        '''
        results = cur.execute(sql)
        count = results.fetchone()[0]
        self.assertGreater(count, 900)

        conn.close()

unittest.main()
