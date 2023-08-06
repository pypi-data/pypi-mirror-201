from . import AbstractParser
from ...models import AnnotationTarget
from .jsonld import JSONLD



class ItemProp(AbstractParser):
    def parse(self, annotation_target: AnnotationTarget, target_url, bs_document, previous_parse_result):
        # Does not change result if previous parse match
        # if previous_parse_result:
        #     return previous_parse_result
        if annotation_target.publication_date is None:
            date_published_element = bs_document.select("[itemProp='datePublished']")
            if date_published_element :
                content = None

                if "content" in date_published_element[0]:
                    content = date_published_element[0]["content"]
                elif "datetime" in date_published_element[0] :
                    content = date_published_element[0]["datetime"]
                else:
                    content = date_published_element[0].string
                if content is not None:
                    date = JSONLD().try_strptimeAll(content)
                    if date is not None:
                        annotation_target.publication_date = date.isoformat()

        if annotation_target.image is None:
            image_element = bs_document.select("[itemProp='image']")
            if image_element:
                image_element_url = None
                if "src" in image_element[0]:
                    image_element_url = image_element[0]["src"]
                elif "content" in image_element[0]:
                    image_element_url = image_element[0]["content"]
                if image_element_url is not None:
                    annotation_target.image = image_element_url

        return True
