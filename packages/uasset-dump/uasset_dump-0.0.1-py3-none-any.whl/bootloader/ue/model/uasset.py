# Copyright (C) 2023 Bootloader.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Bootloader or one of its subsidiaries.  You shall not disclose this
# confidential information and shall use it only in accordance with the
# terms of the license agreement or other applicable agreement you
# entered into with Bootloader.
#
# BOOTLOADER MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE
# SUITABILITY OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR
# A PARTICULAR PURPOSE, OR NON-INFRINGEMENT.  BOOTLOADER SHALL NOT BE
# LIABLE FOR ANY LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF
# USING, MODIFYING OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.


class UAsset:
    def __init__(
            self,
            asset_name: str,
            asset_class_path: str,
            package_name: str,
            dependencies: list[str] or None):
        """
        Build a new {@link UAsset}.


        @param asset_name: The name of the asset without the package.

        @param asset_class_path: The path name of the asset’s class.

        @param package_name: The name of the package in which the asset is
            found.

        @param dependencies: The list of names of the packages that the asset
            depends on.
        """
        self.__asset_name = asset_name
        self.__asset_class_path = asset_class_path
        self.__package_name = package_name
        self.__dependencies = dependencies

    @property
    def asset_class_path(self) -> str:
        """
        Return the path name of the asset's class.

        Examples:

        ```text
        /Script/Engine/SkeletalMesh
        /Script/Engine/Skeleton
        /Script/Engine/Texture2D
        ```

        @return: The path name of the asset's class.
        """
        return self.__asset_class_path

    @property
    def asset_name(self) -> str:
        """
        Return the name of the asset.


        @return: The name of the asset without the package.
        """
        return self.__asset_name

    @property
    def dependencies(self) -> list[str] or None:
        """
        Return the list of names of the packages that the asset depends on.


        @return: The list of names of the packages that the asset depends on.
        """
        return self.__dependencies

    def to_json(self) -> any:
        return {
            "asset_name": self.__asset_name,
            "asset_class_path": self.__asset_class_path,
            "package_name": self.__package_name,
            "dependencies": self.__dependencies
        }

    @property
    def package_name(self) -> str:
        """
        Return the name of the package in which the asset is found.


        @return: The name of the package in which the asset is found.
        """
        return self.__package_name
