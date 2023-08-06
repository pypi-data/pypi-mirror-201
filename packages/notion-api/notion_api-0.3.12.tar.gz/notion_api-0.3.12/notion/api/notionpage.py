# MIT License

# Copyright (c) 2023 ayvi-0001

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

from datetime import datetime
from functools import cached_property
from typing import TYPE_CHECKING, Any, MutableMapping, Optional, Sequence, Union, cast

from notion.api.blockmixin import _TokenBlockMixin
from notion.api.client import _NLOG
from notion.api.notionblock import Block
from notion.api.notiondatabase import Database
from notion.exceptions.errors import NotionInvalidJson
from notion.properties.build import build_payload
from notion.properties.common import Parent, UserObject, _NotionUUID
from notion.properties.files import ExternalFile, FilesPropertyValue, InternalFile
from notion.properties.propertyobjects import Option
from notion.properties.propertyvalues import (
    CheckboxPropertyValue,
    DatePropertyValue,
    EmailPropertyValue,
    MultiSelectPropertyValue,
    NumberPropertyValue,
    PeoplePropertyValue,
    PhoneNumberPropertyValue,
    Properties,
    RelationPropertyValue,
    RichTextPropertyValue,
    SelectPropertyValue,
    StatusPropertyValue,
    TitlePropertyValue,
    URLPropertyValue,
)
from notion.properties.richtext import RichText

if TYPE_CHECKING:
    from datetime import timedelta

__all__: Sequence[str] = ["Page"]


class Page(_TokenBlockMixin):
    """
    The Page object contains the page property values of a single Notion page.
    All pages have a Parent. If the parent is a database, 
    the property values conform to the schema laid out in the database's properties. 
    Otherwise, the only property value is the title.

    Page content is available as blocks:
        - Read using retrieve block children.
        - Appended using append block children.

    NOTE: The current version of the Notion api does not allow pages to be created to the parent `workspace`. 
    Objects created through the API must be created with a parent of an existing Page/Database/Block.

    ---
    ### Versioning:
    To use a previous version of the API, set the envrionment variable `NOTION_VERSION`.
    For more info see: https://developers.notion.com/reference/versioning

    ---
    :param id: (required) `page_id` of object in Notion.
    :param token: Bearer token provided when you create an integration.\
                  Set notion secret in environment variables as `NOTION_TOKEN`, or set variable here.\
                  See https://developers.notion.com/reference/authentication.

    https://developers.notion.com/reference/page
    """

    def __init__(
        self,
        id: str,
        /,
        *,
        token: Optional[str] = None,
    ) -> None:
        super().__init__(id, token=token)
        self.logger = _NLOG.getChild(self.__repr__())

    @classmethod
    def create(
        cls, parent_instance: Union[Page, Database, Block], page_title: str
    ) -> Page:
        """
        Creates a blank page.
        Use Page methods to add values to properties described in parent database schema.
        Add content to page by appending block children with notion.api.blocktypefactory.BlockFactory.

        ---
        :param parent_instance: (required) eithr a Page or Database instance.
        :param page_title: (required)
        :param icon_url: (optional) #not yet implemented
        :param cover: (optional) #not yet implemented

        https://developers.notion.com/reference/post-page
        """
        if "child_database" in parent_instance.type:
            payload = build_payload(
                Parent.database(parent_instance.id),
                Properties(TitlePropertyValue([RichText(page_title)])),
            )
        else:
            payload = build_payload(
                Parent.page(parent_instance.id),
                Properties(TitlePropertyValue([RichText(page_title)])),
            )

        new_page = cls._post(parent_instance, cls._pages_endpoint(), payload=payload)

        cls_ = cls(new_page["id"])
        cls_.logger.debug(
            f"Page created in {parent_instance.__repr__()}. Url: {new_page['url']}"
        )
        return cls_

    def __getitem__(self, property_name: str) -> MutableMapping[str, Any]:
        if property_name in self.properties:
            return cast(MutableMapping[str, Any], self.properties[property_name])
        raise NotionInvalidJson(f"{property_name} not found in page property values.")

    @cached_property
    def _retrieve(self) -> MutableMapping[str, Any]:
        return self.retrieve(filter_properties=None)

    @cached_property
    def properties(self) -> MutableMapping[str, Any]:
        return cast(MutableMapping[str, Any], self._retrieve["properties"])

    @property
    def title(self) -> str:
        try:
            if ("workspace" or "page_id") in self.parent_type:
                return cast(str, self.properties["title"]["title"][0]["plain_text"])

            database_title_property = self.properties[
                [k for k, v in self.properties.items() if "title" in v][0]
            ]
            return cast(str, database_title_property["title"][0]["plain_text"])
        except IndexError:
            return ""  # title is empty

    @title.setter
    def title(self, __new_title: str) -> None:
        self._patch_properties(
            payload=Properties(TitlePropertyValue([RichText(__new_title)]))
        )

    @property
    def url(self) -> str:
        return cast(str, self._retrieve["url"])

    @property
    def icon(self) -> MutableMapping[str, Any]:
        return cast(MutableMapping[str, Any], self._retrieve["icon"])

    @property
    def cover(self) -> MutableMapping[str, Any]:
        return cast(MutableMapping[str, Any], self._retrieve["cover"])

    @property
    def delete_self(self) -> None:
        if self.is_archived:
            self.logger.debug("delete_self did nothing. Page is already archived.")
            return None

        self._delete(self._block_endpoint(self.id))
        self.logger.debug("Deleted self.")

    @property
    def restore_self(self) -> None:
        if not self.is_archived:
            self.logger.debug("restore_self did nothing. Page is not archived.")
            return None

        self._patch(self._pages_endpoint(self.id), payload=(b'{"archived": false}'))
        self.logger.debug("Restored self.")

    def retrieve(
        self, *, filter_properties: Optional[list[str]] = None
    ) -> MutableMapping[str, Any]:
        """ 
        Retrieves a Page object using the ID specified.

        :param filter_properties: (optional) A list of page property value IDs associated with the page.\
                                   Use this param to limit the response to a specific page property value or values.\
                                   To retrieve multiple properties, specify each page property ID.\
                                   E.g. ?filter_properties=iAk8&filter_properties=b7dh.

        https://developers.notion.com/reference/retrieve-a-page
        """
        if filter_properties:
            _pages_endpoint_filtered_prop = f"{self._pages_endpoint(self.id)}?"
            for name in filter_properties:
                name_id = self.properties[name]["id"]
                _pages_endpoint_filtered_prop += f"filter_properties={name_id}&"
            return self._get(_pages_endpoint_filtered_prop)

        return self._get(self._pages_endpoint(self.id))

    def _retrieve_property_id(self, property_name: str) -> str:
        """Internal function to retrieve the id of a property."""
        if property_name in self.properties:
            return str(self.properties[property_name]["id"])
        raise NotionInvalidJson("Property name not found in parent schema.")

    def retrieve_property_item(
        self,
        property_name: str,
    ) -> MutableMapping[str, Any]:
        """
        Retrieves a property_item object for a given page_id and property_id.
        The object returned will either be:
            - a value.
            - a paginated list of property item values.

        :param property_name: (required) property name in Notion *case-sensitive\
                               this endpoint only works with property_id's, internal function will retrieve this.

        https://developers.notion.com/reference/retrieve-a-page-property
        """
        return self._get(
            self._pages_endpoint(
                self.id,
                properties=True,
                property_id=self._retrieve_property_id(property_name),
            )
        )

    def _patch_properties(
        self, payload: MutableMapping[str, Any]
    ) -> MutableMapping[str, Any]:
        """
        Updates page property values for the specified page.
        Properties not set via the properties parameter will remain unchanged.
        If parent is a database, new property values must conform to the parent database's property schema.

        https://developers.notion.com/reference/patch-page
        """
        return self._patch(self._pages_endpoint(self.id), payload=payload)

    def retrieve_page_content(
        self,
        start_cursor: Optional[str] = None,
        page_size: Optional[int] = None,
    ) -> MutableMapping[str, Any]:
        """
        Returns only the first level of children for the specified block.
        See block objects for more detail on determining if that block has nested children.
        In order to receive a complete representation of a block, you
        may need to recursively retrieve block children of child blocks.

        https://developers.notion.com/reference/get-block-children
        """
        return self._get(
            self._block_endpoint(
                self.id, children=True, page_size=page_size, start_cursor=start_cursor
            )
        )

    def _append(self, payload: MutableMapping[str, Any]) -> MutableMapping[str, Any]:
        """
        Used internally by notion.api.blocktypefactory.BlockFactory.

        https://developers.notion.com/reference/patch-block-children
        """
        return self._patch(self._block_endpoint(self.id, children=True), payload=payload)

    def set_select(self, property_name: str, /, select_option: str) -> None:
        """
        :param select_option: (required) if the option already exists, then it is\
                               case sensitive. if the option does not exist, it will be created.
        
        https://developers.notion.com/reference/page-property-values#select
        """
        parent_db = Database(
            self.parent_id,
            token=self.token,
        )

        current_options = parent_db[property_name]["select"]["options"]
        names = {o.get("name"): o.get("color") for o in current_options}

        if set([select_option]).issubset(names):
            option = Option(select_option, names.get(select_option))
        else:
            option = Option(select_option)

        self._patch_properties(Properties(SelectPropertyValue(property_name, option)))

    def set_multiselect(
        self, property_name: str, /, multi_select_options: list[str]
    ) -> None:
        """
        :param multi_select_options: (required) list of strings for each select option.\
                                      if the option already exists, then it is case sensitive.\
                                      if the option does not exist, it will be created.

        https://developers.notion.com/reference/page-property-values#multi-select
        """
        selected_options: list[Option] = []

        parent_db = Database(
            self.parent_id,
            token=self.token,
        )

        current_options = parent_db[property_name]["multi_select"]["options"]
        names = {o.get("name"): o.get("color") for o in current_options}

        for option in multi_select_options:
            if set([option]).issubset(names):
                selected_options.append(Option(option, names.get(option)))
            else:
                selected_options.append(Option(option))

        self._patch_properties(
            Properties(MultiSelectPropertyValue(property_name, selected_options))
        )

    def set_status(self, property_name: str, /, status_option: str) -> None:
        """
        :param status_option: (required) unlike select/multi-select,\
                               status option must already exist when using this endpoint.\
                               to create a new status option, use the database endpoints.\
                               option is case-sensitive.

        https://developers.notion.com/reference/page-property-values#status
        """
        parent_db = Database(
            self.parent_id,
            token=self.token,
        )

        current_options = parent_db[property_name]["status"]["options"]
        names = {o.get("name"): o.get("color") for o in current_options}

        if set([status_option]).issubset(names):
            option = Option(status_option, names.get(status_option))
        else:
            option = Option(status_option)

        self._patch_properties(Properties(StatusPropertyValue(property_name, option)))

    def set_date(
        self,
        property_name: str,
        /,
        start: Union[str, datetime],
        end: Optional[Union[str, datetime]] = None,
    ) -> None:
        """
        :param start: (required) A date, with an optional time.\
                       If the "date" value is a range, then start represents the start of the range.
        :param end: (optional) A string representing the end of a date range.\
                     If the value is null, then the date value is not a range.

        https://developers.notion.com/reference/page-property-values#date
        """
        if isinstance(start, datetime):
            start = start.astimezone(self.tz)
        if end and isinstance(end, datetime):
            end = end.astimezone(self.tz)

        self._patch_properties(
            Properties(DatePropertyValue(property_name, start=start, end=end))
        )

    def set_text(self, property_name: str, /, new_text: Union[str, Any]) -> None:
        """https://developers.notion.com/reference/page-property-values#rich-text"""
        self._patch_properties(
            Properties(RichTextPropertyValue(property_name, [RichText(new_text)]))
        )

    def set_files(
        self,
        property_name: str,
        /,
        array_of_files: Sequence[Union[InternalFile, ExternalFile]],
    ) -> None:
        """
        When updating a file property, the value is overwritten by the array of files passed.
        Although Notion doesn't support uploading files, if you pass a file object containing a file hosted by Notion,
        it remains one of the files. To remove any file, just don't pass it in the update response.

        InternalFiles are a file object corresponding to a file that has been uploaded to Notion.
        ExternalFiles are a file object corresponding to an external file that has been linked to in Notion.

        ---
        :param array_of_files: (required) An array of objects containing information about the files.\
                                Either InternalFile(), ExternalFile() or a combination of both.

        https://developers.notion.com/reference/page-property-values#files
        """
        self._patch_properties(
            Properties(FilesPropertyValue(property_name, array_of_files))
        )

    def set_phone_number(self, property_name: str, /, phone_number: str) -> None:
        """https://developers.notion.com/reference/page-property-values#phone-number"""
        self._patch_properties(
            Properties(PhoneNumberPropertyValue(property_name, phone_number))
        )

    def set_related(self, property_name: str, /, related_ids: Sequence[str]) -> None:
        """
        :param related_ids: (required) An array of related page references.\
                             A page reference is an object with an id key and a string value (UUIDv4)\
                             corresponding to a page ID in another database.
        
        https://developers.notion.com/reference/page-property-values#relation
        """
        list_ids: list[_NotionUUID] = []
        for id in related_ids:
            list_ids.append(_NotionUUID(id))

        self._patch_properties(Properties(RelationPropertyValue(property_name, list_ids)))

    def set_checkbox(self, property_name: str, /, value: bool) -> None:
        """https://developers.notion.com/reference/page-property-values#checkbox"""
        self._patch_properties(Properties(CheckboxPropertyValue(property_name, value)))

    def set_number(
        self, property_name: str, /, new_number: Union[float, timedelta]
    ) -> None:
        """https://developers.notion.com/reference/page-property-values#number"""
        self._patch_properties(Properties(NumberPropertyValue(property_name, new_number)))

    def set_people(self, property_name: str, /, user_array: Sequence[UserObject]) -> None:
        """https://developers.notion.com/reference/page-property-values#people"""
        self._patch_properties(Properties(PeoplePropertyValue(property_name, user_array)))

    def set_email(self, property_name: str, /, email: str) -> None:
        """https://developers.notion.com/reference/page-property-values#email"""
        self._patch_properties(Properties(EmailPropertyValue(property_name, email)))

    def set_url(self, property_name: str, /, url: str) -> None:
        """https://developers.notion.com/reference/page-property-values#url"""
        self._patch_properties(Properties(URLPropertyValue(property_name, url)))
