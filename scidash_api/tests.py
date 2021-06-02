import quantities as pq
from neuronunit.capabilities import ProducesSpikes
import sciunit

# A new M2M test which will compare the equality of spike counts across models
class RandomTest(sciunit.Test):
    required_capabilities = (ProducesSpikes,)
    score_type = sciunit.scores.ZScore
    url = 'http://test-url.com'

    units = pq.UnitQuantity('megaohm', pq.ohm*1e6, symbol='Mohm')  # Megaohms

    observation_schema = [("Mean, Standard Deviation, N",
                           {'mean': {'units': True, 'required': True},
                            'std': {'units': True, 'min': 0, 'required': True},
                            'n': {'type': 'integer', 'min': 1}}),
                          ("Mean, Standard Error, N",
                           {'mean': {'units': True, 'required': True},
                            'sem': {'units': True, 'min': 0, 'required': True},
                            'n': {'type': 'integer', 'min': 1,
                                  'required': True}})]

    def generate_prediction(self,model):
        count = model.get_spike_count()
        return 1*pq.MOhm
