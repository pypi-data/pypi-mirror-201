from utah.core.navigation import BaseNavigationService
from utah.core.navigation import NavigationLoadException
from utah.core.navigation import RootNavItem
from utah.core.navigation import ParentNavItem
from utah.core.navigation import ChildNavItem

import yaml
from yaml import loader
import logging

logger = logging.getLogger(__name__)

class NavigationService(BaseNavigationService):
    def __init__(self, main_microsite:str, reload_interval_secs:int, root_dir:str, nav_path_pattern:str):
        self.nav_file_path_pattern = root_dir + "/" + nav_path_pattern
        BaseNavigationService.__init__(self, main_microsite, reload_interval_secs)


    def load_nav_tree(self):
        (raw_tree, raw_translations) = self.__load_raw_nav_tree(self.main_microsite)
        
        (microsite, description, uri) = self.get_node_header(self.main_microsite, raw_tree)

        if microsite != self.main_microsite:
            raise NavigationLoadException("Home uri's:[%s] microsite does not match microsite of navigation tree:[%s]" % (uri, self.main_microsite))

        translations = {}
        if raw_translations:
            self.add_raw_translations(translations, raw_translations)

        navItem = RootNavItem(raw_tree["description"], uri, translations)

        if "children" in raw_tree:
            self.process_children(microsite, navItem, raw_tree["children"], translations)

        return navItem

    def add_raw_translations(self, translations, raw_translations):
        for locale_key in raw_translations.keys():
            translation_table = None
            locales_raw_translations = raw_translations[locale_key]
            if locale_key in translations:
                translation_table = translations[locale_key]
            else:
                translation_table = {}
                translations[locale_key] = translation_table

            for translation in locales_raw_translations:
                try:
                    source_text = translation["source_text"]
                    translation_text = translation["translation"]

                    if not source_text in translation_table:
                        translation_table[source_text] = translation_text
                except KeyError as e:
                    raise NavigationLoadException("Key error loading translation:[" +  str(translation) + "]. missing key:[" + str(e) + "]")

    def __load_raw_nav_tree(self, microsite:str, main_microsite=False):
        try:
            f = open(self.nav_file_path_pattern % microsite, 'r', encoding="utf-8")
            raw_tree = yaml.load(f, Loader=loader.Loader)
            raw_translations = None
            if "translations" in raw_tree:
                raw_translations = raw_tree["translations"]
            else:
                raw_translations = {}

            f.close()
        except Exception as e:
            if main_microsite:
                raise NavigationLoadException("Malformed json navigation for microsite:[%s]" % microsite)
            else:
                raise e

        return (raw_tree, raw_translations)


    def process_children(self, microsite, curr_nav_item:ParentNavItem, raw_children:list, translations):
        for raw_child in raw_children:
            raw_to_process = raw_child
            microsite_being_processed = microsite

            if "microsite" in raw_child:
                microsite_being_processed = raw_child["microsite"]
                try:
                    raw_to_process = None
                    raw_translations = None
                    (raw_to_process, raw_translations) = self.__load_raw_nav_tree(microsite_being_processed)
                    if raw_translations:
                        self.add_raw_translations(translations, raw_translations)
                except FileNotFoundError as e:
                    logger.warning("Could not locate navigation.yaml for microsite:[%s]" % microsite_being_processed)
                    pass

            if raw_to_process:
                (child_microsite,  child_description, child_uri) = self.get_node_header(microsite, raw_to_process)
                child_nav_item = ChildNavItem(child_description, child_uri, curr_nav_item)

                if "children" in raw_to_process:
                    self.process_children(microsite_being_processed, child_nav_item, raw_to_process["children"], translations)

        return