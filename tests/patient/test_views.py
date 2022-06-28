import pytest

from unittest.mock import sentinel
from django.urls import reverse

from clinician import urls as clinician_urls


class TestBookClinicianAvailabilityViewset:

    @pytest.fixture(autouse=True)
    def _setup(self, clinician_app, mocker):
        self.view = f"{clinician_app}.views"
        self.mocker = mocker

    @pytest.fixture
    def booking_serializer_mock(self):
        return self.mocker.patch(f"{self.view}.BookingSerializer")

    @pytest.fixture
    def booking_model_mock(self):
        return self.mocker.patch(f"{self.view}.Booking")

    @pytest.fixture
    def response_mock(self):
        return self.mocker.patch(f"{self.view}.Response")

    def test_create(self, booking_serializer_mock, rf):
        # rf is the request factory fixture provided in pytest-django
        url = reverse("book_clinician_availability", kwargs={'clinician_id': "clinician_id"})
        request_data = {"data": 1}
        request = rf.post(
            url,
            content_type='application/json',
            data=request_data
        )

        booking_serializer_mock.return_value.is_valid.return_value = True
        booking_serializer_mock.return_value.data = request_data
        # response_mock.return_value = Response(request_data, status=201, content_type="application/json")

        view = clinician_urls.book_clinician_availability
        actual_output = view(request, sentinel.clinician_id).render()

        # actual_output = self.client.post(
        #     url,
        #     content_type='application/json',
        #     data={"data": 1}
        # )

        assert actual_output.data == request_data
        assert actual_output.status_code == 201
        booking_serializer_mock.assert_called_once_with(data=request_data)
        booking_serializer_mock.return_value.is_valid.assert_called_once()
        booking_serializer_mock.return_value.save.assert_called_once()


    def test_create_failure(self, booking_serializer_mock, rf):
        request_data = {"data": 1}
        url = reverse("book_clinician_availability", kwargs={'clinician_id': "clinician_id"})
        request = rf.post(
            url,
            content_type='application/json',
            data=request_data
        )

        booking_serializer_mock.return_value.is_valid.side_effect = Exception
        view = clinician_urls.book_clinician_availability
        with pytest.raises(Exception):
            view(request, sentinel.clinician_id).render()

        booking_serializer_mock.assert_called_once_with(data=request_data)
        booking_serializer_mock.return_value.is_valid.assert_called_once()

    def test_list(self, booking_model_mock, booking_serializer_mock, rf):
        url = reverse("book_clinician_availability", kwargs={'clinician_id': "clinician_id"})
        request = rf.get(
            url,
            content_type='application/json'
        )
        booking_model_mock.get_clinician_booking_list.return_value = sentinel.queryset
        booking_data = {"data": 1}
        booking_serializer_mock.return_value.data = booking_data
        view = clinician_urls.book_clinician_availability
        actual_output = view(request, sentinel.clinician_id).render()
        assert actual_output.data == booking_data
        assert actual_output.status_code == 200
