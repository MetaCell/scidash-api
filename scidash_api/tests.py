from neuronunit.capabilities import ProducesSpikes
import sciunit

# A new M2M test which will compare the equality of spike counts across models
class RandomTest(sciunit.Test):
    required_capabilities = (ProducesSpikes,)
    score_type = sciunit.scores.ZScore
    url = 'http://test-url.com'
    def generate_prediction(self,model):
        count = model.get_spike_count()
        return count
