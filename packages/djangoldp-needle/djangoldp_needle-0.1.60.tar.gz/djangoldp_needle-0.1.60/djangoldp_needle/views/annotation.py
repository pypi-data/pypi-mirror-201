from django.core.exceptions import SuspiciousOperation
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Count
from djangoldp.serializers import LDPSerializer
from djangoldp.views import LDPViewSet, LDPNestedViewSet
from djangoldp_account.models import LDPUser
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from ..request_parser.webdriver_utils import get_webdriver

from ..models import Annotation, NeedleActivity, AnnotationTarget, Tag
from ..models.needle_activity import ACTIVITY_TYPE_FIRST_ANNOTATION_WITH_CONNECTIONS, \
    ACTIVITY_TYPE_FIRST_ANNOTATION_WITHOUT_CONNECTIONS
import json
# from selenium import webdriver
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from django.db.models import Q, F

import random
import string
import requests as requestsLib
from ..request_parser import RequestParser
from requests.exceptions import ReadTimeout, ConnectionError
import re
import time
import datetime


# from django.conf import settings

class AnnotationSerializer(LDPSerializer):
    def to_representation(self, obj):
        rep = super().to_representation(obj)
        if hasattr(obj, "local_intersection_after"):
            rep['local_intersection_after'] = obj.local_intersection_after
        if hasattr(obj, "local_intersection_before"):
            rep['local_intersection_before'] = obj.local_intersection_before

        return rep


class AnnotationViewset(LDPViewSet):
    serializer_class = AnnotationSerializer
    fields = ['@id', 'creator', 'creation_date', 'annotation_date', 'target', 'tags', 'description', 'booklets']

    def is_safe_create(self, user, validated_data, *args, **kwargs):
        # TODO: check new annotation owner by current user

        target_url_id = validated_data['target']['urlid']
        user_annotation_with_same_target_count = Annotation.objects.filter(creator=user).filter(
            target__urlid=target_url_id).count()

        if user_annotation_with_same_target_count > 0:
            raise ValidationError({'Attention': ['Vous avez déjà cette ressource dans votre fil.']})
        return True

    def get_queryset(self, *args, **kwargs):
        qs = Annotation.objects
        if 'slug' in self.kwargs:
            param_user = LDPUser.objects.get(slug=self.kwargs['slug'])
            qs = qs.filter(creator=param_user)

        qs = qs.annotate(
            local_intersection_after=Count('target__annotations',
                                           filter=Q(target__annotations__annotation_date__gt=F("annotation_date"))),
            local_intersection_before=Count('target__annotations',
                                            filter=Q(target__annotations__annotation_date__lt=F("annotation_date"))),
        )

        return qs


#
# def init_webdriver():
#     firefoxOptions = webdriver.FirefoxOptions()
#     firefoxOptions.headless = True
#     path = settings.BROWSER_PATH
#     driver = webdriver.Firefox(firefox_binary=FirefoxBinary(path)
#                                , options=firefoxOptions
#                                )
#     # chromeOptions = webdriver.ChromeOptions()
#     # chromeOptions.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
#     # chromeOptions.add_argument("--no-sandbox")
#     # chromeOptions.add_argument("--disable-setuid-sandbox")
#     # chromeOptions.add_argument("--disable-dev-shm-usage")
#     # chromeOptions.add_argument("--disable-extensions")
#     # chromeOptions.add_argument("--disable-gpu")
#     # chromeOptions.add_argument("start-maximized")
#     # chromeOptions.add_argument("disable-infobars")
#     # chromeOptions.add_argument("--headless")
#     # driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
#     #                           options=chromeOptions)
#     return driver
#

def import_external_annotations(external_annotations, annotation_tags_separator):
    driver = get_webdriver()
    index = 0
    for external_annotation in external_annotations:
        index = index + 1
        user_name = None
        if "user_name" in external_annotation:
            user_name = external_annotation["user_name"]
        user_email = external_annotation["user_email"]
        user_creation_date = external_annotation["user_creation_date"]
        target_url = external_annotation["target_url"]
        target_title = external_annotation["target_title"]
        target_creation_date = external_annotation["target_creation_date"]
        annotation_description = external_annotation["annotation_description"]
        annotation_date = external_annotation["annotation_date"]
        if "annotation_tags" in external_annotation:
            annotation_tags = external_annotation["annotation_tags"]
        else:
            annotation_tags = extract_tags_from_text(annotation_description)

        import_external_annotation(user_name, user_email, user_creation_date, target_url, target_title,
                                   target_creation_date, annotation_description, annotation_date, annotation_tags,
                                   annotation_tags_separator, driver)
    print("annotations treated :" + str(index))
    driver.quit()


def extract_tags_from_text(text):
    return ' '.join(re.findall(r'#\w+', text))


def import_external_annotation(user_name, user_email, user_creation_date, target_url, target_title,
                               target_creation_date, annotation_description, annotation_date, annotation_tags,
                               annotation_tags_separator, driver):
    annotation = None

    user = None
    print("[USER] " + user_email)
    user_email = user_email.lower()
    try:
        user = LDPUser.objects.get(email=user_email)
    except ObjectDoesNotExist:
        print("")
    if user is None:
        print("[USER] NEW " + user_email)
        password = ''.join(random.choices(string.ascii_lowercase, k=5))
        if not (user_name and user_name.strip()):
            timestamp = int(time.time())
            user_name = "Chenille_" + str(timestamp)

        slug = user_name.strip().replace(" ", "_").lower()

        user = LDPUser(email=user_email, first_name='', last_name='',
                       username=slug,
                       password=password,
                       date_joined=user_creation_date,
                       slug=slug
                       )
        user.save()
    else:
        print("user already exists")

    target = None

    targetUrl = target_url

    print("[TARGET] " + targetUrl)
    try:
        target = AnnotationTarget.objects.get(target=targetUrl)
    except ObjectDoesNotExist:
        print("")

    target_content = None

    if target is None:

        target_request_response = False
        try:
            target_request_response = requestsLib.get(targetUrl, verify=False,
                                                      allow_redirects=True, timeout=10)
            print("target request response code  " + str(target_request_response.status_code))
        except ReadTimeout:
            target_request_response = False
        except ConnectionError:
            target_request_response = False
        if not target_request_response or target_request_response.status_code >= 300:
            print("target new use request failed -> use selenium ")
            new_driver = False
            try:
                # driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
                #                           options=chromeOptions)
                if driver is None:
                    new_driver = True
                    driver = get_webdriver()
                driver.get(targetUrl)
                WebDriverWait(driver, 10).until(
                    expected_conditions.presence_of_element_located((By.TAG_NAME, "body")))
                target_content = driver.page_source
            except TimeoutException:
                print("TimeoutException")
            except WebDriverException:
                print("WebDriverException")
            finally:
                if driver is not None and new_driver:
                    driver.close()
                    driver = None

        else:
            target_content = target_request_response.content

        if target_content is not None:
            print("[TARGET_CONTENT] not None")
            parser = RequestParser()
            (result, annotation_target) = parser.parse(targetUrl, target_content)
            try:
                annotation_target_tmp = AnnotationTarget.objects.get(target=annotation_target.target)
                print("existing target")
                annotation_target = annotation_target_tmp
            except ObjectDoesNotExist:
                print("no existing target")
                print("[TARGET] NEW " + annotation_target.target)
                annotation_target.annotation_target_date = target_creation_date
                annotation_target.save()
            target = annotation_target
        else:
            print("")

    if target is not None:
        if not (target.annotation_target_date == target_creation_date):
            target_creation_date_datetime = datetime.datetime.strptime(target_creation_date, "%Y-%m-%d %H:%M:%S")
            if not target.annotation_target_date:
                target.annotation_target_date = target_creation_date
                target.save()
            else :
                current_date = target.annotation_target_date.strftime("%Y-%m-%d %H:%M:%S")
                if current_date>target_creation_date :
                    target.annotation_target_date = target_creation_date
                    target.save()

        tags = None

        if annotation_tags is not None:
            print("has tags " + annotation_tags)
            tags = []
            for tagname in annotation_tags.split(annotation_tags_separator):
                print("has tag " + tagname)
                if len(tagname) > 0:
                    tagname = tagname.strip()
                    if len(tagname) > 0:
                        if tagname.startswith("#"):
                            tagname = tagname[1:].strip()
                        if len(tagname) > 0:
                            tag = None
                            try:
                                tag = Tag.objects.get(name=tagname,
                                                      creator=user)
                                tags.append(tag)
                            except ObjectDoesNotExist:
                                print("")
                            if tag is None:
                                print("[TAG] NEW " + tagname)
                                tag = Tag(name=tagname,
                                          creator=user)
                                tag.save()
                                tags.append(tag)
                            else:
                                print("tag already exists")

        user_annotation_with_same_target_count = Annotation.objects.filter(creator=user, target=target).count()
        if user_annotation_with_same_target_count == 0:
            print("[ANNOTATION] NEW ")
            if tags is None:
                annotation = Annotation(annotation_date=annotation_date,
                                        target=target,
                                        creator=user,
                                        description=annotation_description)
            else:
                annotation = Annotation(annotation_date=annotation_date,
                                        target=target,
                                        creator=user,
                                        description=annotation_description)
            annotation.save()
            if tags is not None:
                for tag in tags:
                    annotation.tags.add(tag)
                annotation.save()
        else:
            print("annotation already exists")
    return annotation
