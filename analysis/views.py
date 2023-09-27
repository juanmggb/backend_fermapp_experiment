from analysis.models import Analysis
from analysis.serializers import AnalysisSerializer

from rest_framework.viewsets import ModelViewSet


class AnalysisViewSet(ModelViewSet):

    queryset = Analysis.objects.all() 

    serializer_class = AnalysisSerializer