from django.core.exceptions import ObjectDoesNotExist
from djangoldp.views import LDPViewSet, JSONLDParser, NoCSRFAuthentication
from rest_framework import status
import requests as requestsLib

from ..models import AnnotationTarget, NeedleActivity
from ..models.needle_activity import ACTIVITY_TYPE_FIRST_ANNOTATION_WITHOUT_CONNECTIONS
from rest_framework.views import APIView, Response

from ..request_parser import RequestParser
from requests.exceptions import ReadTimeout, ConnectionError
from ..request_parser.webdriver_utils import get_webdriver

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

class AnnotationTargetViewset(LDPViewSet):
    def create(self, request, *args, **kwargs):
        self.check_model_permissions(request)
        target = request.data['target']
        try:
            targets_in_db = AnnotationTarget.objects.get(target=target)
        except ObjectDoesNotExist:
            try:
                new_annotation = self.parse_target(target)
                return self.save_annotation_target(request, new_annotation)

            except Exception as e:
                return self.generate_invalide_response()

        return self.generate_success_response(status.HTTP_200_OK, targets_in_db)

    def parse_target(self, target):
        target_content = None
        try :
            targetRequestResponse = requestsLib.get(target, verify=False, allow_redirects=True, timeout=10)
            # target_content = targetRequestResponse.content
        # if targetRequestResponse.status_code != 200:
        #     raise Exception

        except ReadTimeout:
            targetRequestResponse = False
        except ConnectionError:
            targetRequestResponse = False
        if not targetRequestResponse or targetRequestResponse.status_code != 200:
            # print("target new use request failed -> use selenium ")
            driver = None
            try:
                # driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
                #                           options=chromeOptions)
                driver = get_webdriver()
                driver.get(target)
                WebDriverWait(driver, 10).until(
                    expected_conditions.presence_of_element_located((By.TAG_NAME, "body")))
                target_content = driver.page_source
            except TimeoutException:
                print("")
            except WebDriverException:
                print("")
            finally:
                if driver is not None:
                    driver.close()
        else:
            target_content = targetRequestResponse.content
        annotation_target = None
        if target_content is None:
            raise Exception

        parser = RequestParser()
        (result, annotation_target) = parser.parse(target, target_content)
        if not result:
            raise Exception

        return annotation_target

    def generate_success_response(self, status, target):
        response_serializer = self.get_serializer()
        data = response_serializer.to_representation(target)
        headers = self.get_success_headers(data)
        return Response(data, status=status, headers=headers)

    def generate_invalide_response(self):
        return Response({'URL': ['Le lien est invalide']}, status=status.HTTP_400_BAD_REQUEST)

    def save_annotation_target(self, request, annotation_target):
        annotation_target.save()
        response_serializer = self.get_serializer()
        data = response_serializer.to_representation(annotation_target)
        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        return Response() # Force empty list to avoid performance issues due to a large dataset