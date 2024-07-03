from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Deal, UserDeal
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime


# Create your views here.
@csrf_exempt
def create_deal(request):
    req = json.loads(request.body)
    deal = Deal(item=int(req.get("item")), price=int(req.get("price")))
    deal_end_at_str = req.get("deal_end_at")
    try:
        deal_end_at = datetime.fromisoformat(deal_end_at_str)
        deal.deal_end_time = deal_end_at
    except Exception as e:
        return JsonResponse(
            {"sucess": False, "msg": "invalid date time format"}, status=400
        )

    deal.save()
    return JsonResponse({"success": True, "deal_id": deal.id})


@csrf_exempt
def update_deal(request):
    req = json.loads(request.body)
    deal_id = req.get("deal_id")
    deal = Deal.objects.filter(id=deal_id).first()
    if deal:
        if req.get("item"):
            deal.item = int(req.get("item"))
        if req.get("deal_end_at"):
            try:
                deal_end_at = datetime.fromisoformat(req.get("deal_end_at"))
                deal.deal_end_time = deal_end_at
            except Exception as e:
                return JsonResponse(
                    {"sucess": False, "msg": "invalid date time format"}, status=400
                )
        deal.save()
        return JsonResponse({"success": True, "msg": "deal updated succesfully"})

    return JsonResponse({"success": False, "msg": "invalid deal id"}, status=400)


@csrf_exempt
def end_deal(request):
    req = json.loads(request.body)
    deal_id = req.get("deal_id")
    Deal.objects.filter(id=deal_id).update(active=False)
    return JsonResponse({"success": True, "msg": f"end deal :{deal_id}"})


@csrf_exempt
def claim_deal(request):
    req = json.loads(request.body)
    deal_id = req.get("deal_id")
    user_id = req.get("user_id")
    time_now = datetime.now()
    deal = Deal.objects.filter(
        id=deal_id, item__gte=1, active=True, deal_end_time__gte=time_now
    ).first()
    if not deal:

        return JsonResponse(
            {"success": False, "msg": "no active deal found"}, status=400
        )
    user_deal = UserDeal.objects.filter(user_id=user_id, deal_id=deal_id).first()

    if user_deal:
        return JsonResponse(
            {"success": False, "msg": "user has already taken this deal"}, status=400
        )

    deal.item = deal.item - 1
    UserDeal.objects.create(user_id=user_id, deal_id=deal_id)
    deal.save()

    return JsonResponse({"success": True, "deal_id": deal.id})


def show_deals(request):
    try:
        deals = Deal.objects.all()
        deal_list = list(deals.values("id", "item", "price", "deal_end_time", "active"))
        return JsonResponse({"items": deal_list})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def show_users(request):
    try:
        user_deals = UserDeal.objects.all()
        user_deals_list = list(user_deals.values("deal_id", "user_id"))
        return JsonResponse({"items": user_deals_list})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
