from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from diagrams.onprem.client import Users
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import RabbitMQ, Celery
from diagrams.programming.framework import Django, FastAPI

with Diagram("Architecture for Notifications", show=False, filename="schemes/notifications", curvestyle="curved"):
    managers = Users("Managers")

    with Cluster("Notifications"):
        postgresql = PostgreSQL("PostgreSQL")
        rabbit_broker = RabbitMQ("Notifications Broker")
        nginx = Nginx("Nginx")
        managers >> nginx

        # Admin
        admin_panel = Django("Admin Panel")
        admin_panel >> postgresql
        nginx >> admin_panel

        # API
        api = FastAPI("API")
        nginx >> api
        api >> postgresql
        api >> rabbit_broker

        # Worker
        worker = Custom("FastStream", "../resources/faststream.svg")
        worker >> rabbit_broker
        worker >> postgresql

        with Cluster("Scheduler"):
            celery_worker = Celery("Celery Worker")
            redis_broker = Redis("Celery Broker")
            celery_beat = Celery("Celery Beat")
            celery_beat >> redis_broker >> celery_worker >> rabbit_broker
            celery_beat >> postgresql
            celery_worker >> postgresql

    profiles_api = FastAPI("Profiles API")
    worker >> profiles_api
