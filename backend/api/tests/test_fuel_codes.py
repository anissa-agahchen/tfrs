# -*- coding: utf-8 -*-
# pylint: disable=no-member,invalid-name
"""
    REST API Documentation for the NRsS TFRS Credit Trading Application

    The Transportation Fuels Reporting System is being designed to streamline
    compliance reporting for transportation fuel suppliers in accordance with
    the Renewable & Low Carbon Fuel Requirements Regulation.

    OpenAPI spec version: v1

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import json

from rest_framework import status

from api.models.FuelCode import FuelCode
from api.models.FuelCodeStatus import FuelCodeStatus
from api.serializers.FuelCode import FuelCodeCreateSerializer

from .base_test_case import BaseTestCase


class TestFuelCodes(BaseTestCase):
    """Tests for the fuel codes endpoint"""
    extra_fixtures = ['test/test_fuel_codes.json']

    def test_get_fuel_code_list(self):
        """
        Test that the fuel codes list loads properly
        """
        # View the organization that fs_user_1 belongs to
        response = self.clients['gov_analyst'].get(
            "/api/fuel_codes"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = json.loads(response.content.decode("utf-8"))

        self.assertGreaterEqual(len(response_data), 1)

        response = self.clients['fs_user_1'].get(
            "/api/fuel_codes"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = json.loads(response.content.decode("utf-8"))

        self.assertGreaterEqual(len(response_data), 1)

    def test_add_draft_as_gov_user(self):
        """
        Test adding a fuel code as a government user
        """
        status_draft = FuelCodeStatus.objects.filter(status="Draft").first()

        payload = {
            'applicationDate': '2019-01-01',
            'approvalDate': '2019-01-01',
            'carbonIntensity': '10',
            'company': 'Test',
            'effectiveDate': '2019-01-01',
            'expiryDate': '2020-01-01',
            'facilityLocation': 'Test',
            'facilityNameplate': '123',
            'feedstock': 'Test',
            'feedstockLocation': 'Test',
            'feedstockMisc': 'Test',
            'feedstockTransportMode': ['Pipeline', 'Truck'],
            'formerCompany': 'Test',
            'fuel': 'LNG',
            'fuelCode': 'BCLCF',
            'fuelCodeVersion': '105',
            'fuelTransportMode': ['Rail'],
            'status': status_draft.id
        }

        response = self.clients['gov_analyst'].post(
            "/api/fuel_codes",
            content_type='application/json',
            data=json.dumps(payload)
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = json.loads(response.content.decode("utf-8"))

        fuel_code_obj = FuelCode.objects.get(id=response_data['id'])

        self.assertEqual(fuel_code_obj.fuel.name, 'LNG')

    def test_add_draft_as_fuel_supplier(self):
        """
        Test adding a fuel code as a fuel supplier
        Note: This should fail
        """
        status_draft = FuelCodeStatus.objects.filter(status="Draft").first()

        payload = {
            'applicationDate': '2019-01-01',
            'approvalDate': '2019-01-01',
            'carbonIntensity': '10',
            'company': 'Test',
            'effectiveDate': '2019-01-01',
            'expiryDate': '2020-01-01',
            'facilityLocation': 'Test',
            'facilityNameplate': '123',
            'feedstock': 'Test',
            'feedstockLocation': 'Test',
            'feedstockMisc': 'Test',
            'feedstockTransportMode': 'Test',
            'formerCompany': 'Test',
            'fuel': 'LNG',
            'fuelCode': 'BCLCF',
            'fuelCodeVersion': '101',
            'fuelCodeVersionMinor': '1',
            'fuelTransportMode': 'Test',
            'status': status_draft.id
        }

        response = self.clients['fs_user_1'].post(
            "/api/fuel_codes",
            content_type='application/json',
            data=json.dumps(payload)
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_draft_as_gov_user(self):
        """
        Test deleting a fuel code as a government analyst
        """
        status_draft = FuelCodeStatus.objects.filter(status="Draft").first()

        data = {
            'application_date': '2019-01-01',
            'approval_date': '2019-01-01',
            'carbon_intensity': '10',
            'company': 'Test',
            'effective_date': '2019-01-01',
            'expiry_date': '2020-01-01',
            'facility_location': 'Test',
            'facility_nameplate': '123',
            'feedstock': 'Test',
            'feedstock_location': 'Test',
            'feedstock_misc': 'Test',
            'feedstock_transport_mode': ['Rail'],
            'former_company': 'Test',
            'fuel': 'LNG',
            'fuel_code': 'BCLCF',
            'fuel_code_version': '110',
            'fuel_code_version_minor': '0',
            'fuel_transport_mode': ['Rail'],
            'status': status_draft.id
        }

        serializer = FuelCodeCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        fuel_code = serializer.save()

        response = self.clients['gov_analyst'].delete(
            "/api/fuel_codes/{}".format(fuel_code.id)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_draft_as_fuel_supplier(self):
        """
        Test deleting a fuel code as a fuel supplier
        Note: This should fail (well, they shouldn't see the code at all)
        """
        status_draft = FuelCodeStatus.objects.filter(status="Draft").first()

        data = {
            'application_date': '2019-01-01',
            'approval_date': '2019-01-01',
            'carbon_intensity': '10',
            'company': 'Test',
            'effective_date': '2019-01-01',
            'expiry_date': '2020-01-01',
            'facility_location': 'Test',
            'facility_nameplate': '123',
            'feedstock': 'Test',
            'feedstock_location': 'Test',
            'feedstock_misc': 'Test',
            'feedstock_transport_mode': ['Rail'],
            'former_company': 'Test',
            'fuel': 'LNG',
            'fuel_code': 'BCLCF',
            'fuel_code_version': '101',
            'fuel_code_version_minor': '2',
            'fuel_transport_mode': ['Rail'],
            'status': status_draft.id
        }

        serializer = FuelCodeCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        fuel_code = serializer.save()

        response = self.clients['fs_user_1'].delete(
            "/api/fuel_codes/{}".format(fuel_code.id)
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_approved(self):
        """
        Test deleting an approved fuel code
        Note: This should fail as you shouldn't be able to delete approved
        fuel codes
        """
        status_approved = FuelCodeStatus.objects.filter(
            status="Approved").first()

        data = {
            'application_date': '2019-01-01',
            'approval_date': '2019-01-01',
            'carbon_intensity': '10',
            'company': 'Test',
            'effective_date': '2019-01-01',
            'expiry_date': '2020-01-01',
            'facility_location': 'Test',
            'facility_nameplate': '123',
            'feedstock': 'Test',
            'feedstock_location': 'Test',
            'feedstock_misc': 'Test',
            'feedstock_transport_mode': ['Rail'],
            'former_company': 'Test',
            'fuel': 'LNG',
            'fuel_code': 'BCLCF',
            'fuel_code_version': '101',
            'fuel_code_version_minor': '2',
            'fuel_transport_mode': ['Rail'],
            'status': status_approved.id
        }

        serializer = FuelCodeCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        fuel_code = serializer.save()

        response = self.clients['gov_analyst'].delete(
            "/api/fuel_codes/{}".format(fuel_code.id)
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_fuel_code_export(self):
        """
        Test that the fuel codes XLS generation returns 200
        """
        # View the organization that fs_user_1 belongs to
        response = self.clients['gov_analyst'].get(
            "/api/fuel_codes/xls"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_fuel_code_validation(self):
        """
        Tests that the serializer throws a proper error when a duplicate
        fuel code is being added.
        It will then test and make sure that we don't skip any version.
        """
        status_approved = FuelCodeStatus.objects.filter(
            status="Approved").first()

        payload = {
            'applicationDate': '2019-01-01',
            'approvalDate': '2019-01-01',
            'carbonIntensity': '10',
            'company': 'Test',
            'effectiveDate': '2019-01-01',
            'expiryDate': '2020-01-01',
            'facilityLocation': 'Test',
            'facilityNameplate': '123',
            'feedstock': 'Test',
            'feedstockLocation': 'Test',
            'feedstockMisc': 'Test',
            'feedstockTransportMode': ['Pipeline', 'Truck'],
            'formerCompany': 'Test',
            'fuel': 'LNG',
            'fuelCode': 'BCLCF',
            'fuelCodeVersion': '100',
            'fuelCodeVersionMinor': '0',
            'fuelTransportMode': ['Rail'],
            'status': status_approved.id
        }

        response = self.clients['gov_analyst'].post(
            "/api/fuel_codes",
            content_type='application/json',
            data=json.dumps(payload)
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        payload['fuelCodeVersionMinor'] = '50'

        response = self.clients['gov_analyst'].post(
            "/api/fuel_codes",
            content_type='application/json',
            data=json.dumps(payload)
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_prevent_fuel_code_update_read_only(self):
        """
        Tests that the serializer prevents the version from being updated as
        it's a read-only field
        """
        fuel_code = FuelCode.objects.get(
            fuel_code="BCLCF",
            fuel_code_version="100",
            fuel_code_version_minor="0"
        )

        payload = {
            'fuelCodeVersion': '110',
            'fuelCodeVersionMinor': '10'
        }

        self.clients['gov_analyst'].put(
            "/api/fuel_codes/{}".format(
                fuel_code.id
            ),
            content_type='application/json',
            data=json.dumps(payload)
        )

        fuel_code = FuelCode.objects.get(
            id=fuel_code.id
        )

        self.assertEqual(fuel_code.fuel_code_version, 100)
        self.assertEqual(fuel_code.fuel_code_version_minor, 0)
