from rest_framework import generics, response, status

from service import serializers, services


class ShipmentAPIView(generics.GenericAPIView):
    serializer_class = serializers.ShipmentListSerializer

    def get(self, request, *args, **kwargs) -> response.Response:
        shipments = services.ShipmentService.get_list(is_deleted=False)
        serializer = self.get_serializer(shipments, many=True)
        return response.Response(
            data={"data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs) -> response.Response:
        serializer = serializers.ShipmentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = services.ShipmentService.create_shipment_by_zip_code(
            weight=serializer.validated_data.get("weight"),
            description=serializer.validated_data.get("description"),
            pick_zip=serializer.validated_data.get("pick_up"),
            delivery_zip=serializer.validated_data.get("delivery"),
        )
        return response.Response(
            data={
                "message": "Shipment was succesfully created",
                "data": serializers.ShipmentCreateSerializer(data).data,
                "status": "Created",
            },
            status=status.HTTP_201_CREATED,
        )


class ShipmentRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = services.ShipmentService.get_list(is_deleted=False)
    serializer_class = serializers.ShipmentRetriveSerializer
    lookup_field = "id"

    def get(self, request, *args, **kwargs) -> response.Response:
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(
            data={
                "message": "Shipment data successfully updated",
                "data": serializers.ShipmentRetriveSerializer(instance).data,
                "status": "Updated",
            }
        )