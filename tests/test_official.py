import unittest
import numpy as np

class OfficialProgressTests(unittest.TestCase):
    def test_progress_reconstructs_each_official_state(self):
        from official_geometry import progress_from_states
        states=[]
        for end in (5,10,15):
            mask=np.zeros((20,20),bool);mask[8:12,1:end]=True;states.append(mask)
        mask,progress,thresholds=progress_from_states(states)
        self.assertTrue(np.array_equal(mask,states[-1]))
        for state,t in zip(states,thresholds):
            self.assertTrue(np.array_equal(mask & (progress<=t),state))
        self.assertLess(progress[9,1],progress[9,4])
        self.assertLess(progress[9,4],progress[9,8])
        self.assertLess(progress[9,8],progress[9,14])

if __name__=='__main__':unittest.main()
