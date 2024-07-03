from django.test import TestCase
from django.urls import reverse
from views import claim_deal
from datetime import datetime


# Create your tests here.


class TestClaimDeal(TestCase):
    def setUp(self):
        self.item1 = Deal.objects.create(
            item=2, active=True, deal_end_time=datetime.now()
        )
        self.url = reverse("claim_deal")
        self.response = self.client.post(self.url)

    def test_success(self):
        
        pass
