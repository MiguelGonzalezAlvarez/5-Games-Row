from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.db.database import get_db
from app.models.models import User
from app.core.security import get_current_user_required

router = APIRouter()


notification_subscriptions: dict = {}


class Subscription(BaseModel):
    user_id: int
    endpoint: str
    keys: dict


class NotificationPayload(BaseModel):
    title: str
    body: str
    icon: Optional[str] = None
    badge: Optional[str] = None
    tag: Optional[str] = None
    data: Optional[dict] = None


@router.post("/subscribe")
async def subscribe(
    subscription: Subscription,
    current_user: User = Depends(get_current_user_required),
    db: Session = Depends(get_db)
):
    """Subscribe to push notifications"""
    if current_user.id not in notification_subscriptions:
        notification_subscriptions[current_user.id] = []
    
    notification_subscriptions[current_user.id].append({
        "endpoint": subscription.endpoint,
        "keys": subscription.keys,
        "subscribed_at": datetime.utcnow().isoformat()
    })
    
    return {"message": "Subscribed successfully"}


@router.post("/unsubscribe")
async def unsubscribe(
    endpoint: str,
    current_user: User = Depends(get_current_user_required)
):
    """Unsubscribe from push notifications"""
    if current_user.id in notification_subscriptions:
        notification_subscriptions[current_user.id] = [
            sub for sub in notification_subscriptions[current_user.id]
            if sub["endpoint"] != endpoint
        ]
    
    return {"message": "Unsubscribed successfully"}


@router.get("/subscriptions")
async def get_subscriptions(
    current_user: User = Depends(get_current_user_required)
):
    """Get user's subscriptions"""
    subs = notification_subscriptions.get(current_user.id, [])
    return {
        "count": len(subs),
        "subscriptions": subs
    }


async def send_notification_to_user(user_id: int, payload: NotificationPayload):
    """Send notification to a specific user"""
    if user_id not in notification_subscriptions:
        return
    
    # In a real implementation, this would use webpush library
    # to send actual push notifications
    for subscription in notification_subscriptions[user_id]:
        # Placeholder for actual push notification sending
        pass


async def broadcast_notification(payload: NotificationPayload):
    """Broadcast notification to all subscribed users"""
    for user_id in notification_subscriptions:
        await send_notification_to_user(user_id, payload)


@router.post("/notify")
async def notify_all(
    payload: NotificationPayload,
    background_tasks: BackgroundTasks
):
    """Send notification to all users (admin endpoint)"""
    background_tasks.add_task(broadcast_notification, payload)
    return {"message": "Notification sent"}


@router.post("/notify/user/{user_id}")
async def notify_user(
    user_id: int,
    payload: NotificationPayload,
    background_tasks: BackgroundTasks
):
    """Send notification to specific user"""
    background_tasks.add_task(send_notification_to_user, user_id, payload)
    return {"message": f"Notification sent to user {user_id}"}
