from statsig_openfeature_provider_python import StatsigProvider


class TestStatsigProvider:
    def test_get_metadata(self):
        provider = StatsigProvider()
        assert provider.get_metadata().name == "StatsigProvider"
