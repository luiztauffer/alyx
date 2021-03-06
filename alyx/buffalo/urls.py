from django.urls import path
from django.contrib.auth.decorators import login_required

from buffalo.views import (
    TaskCreateView,
    getTaskCategoryJson,
    TaskCreateVersionView,
    SessionDetails,
    SubjectDetailView,
    ElectrodeBulkLoadView,
    ElectrodeLogBulkLoadView,
    ChannelRecordingBulkLoadView,
    PlotsView,
    SessionQueriesView,
    SessionsLoadView,
    TasksLoadView,
    FoodWeightView,
    ElectrodeLogPlotView,
    TaskPlotView,
    ElectrodeStatusPlotView,
    getSubjectJson,
)

urlpatterns = [
    path("buffalo-tasks/", TaskCreateView.as_view(), name="buffalo-tasks"),
    path(
        "buffalo-get-task-category-json/",
        login_required(getTaskCategoryJson.as_view(), login_url="/login/",),
        name="buffalo-get-task-category-json",
    ),
    path(
        "buffalo-task-version/<uuid:pk>/",
        login_required(TaskCreateVersionView.as_view(), login_url="/login/",),
        name="buffalo-task-version",
    ),
    path(
        "daily-observation/<uuid:subject_id>",
        login_required(SubjectDetailView.as_view(), login_url="/login/",),
        name="daily-observation",
    ),
    path(
        "session-details/<uuid:session_id>",
        login_required(SessionDetails.as_view(), login_url="/login/",),
        name="session-details",
    ),
    path(
        "electrode-bulk-load/<uuid:device_id>",
        login_required(ElectrodeBulkLoadView.as_view(), login_url="/login/",),
        name="electrode-bulk-load",
    ),
    path(
        "electrodelog-bulk-load/<uuid:subject_id>",
        login_required(
            ElectrodeLogBulkLoadView.as_view(),
            login_url='/login/',
        ),
        name="electrodelog-bulk-load",
    ),
    path(
        "channelrecord-bulk-load/<uuid:subject_id>",
        login_required(
            ChannelRecordingBulkLoadView.as_view(),
            login_url='/login/',
        ),
        name="channelrecord-bulk-load",
    ),
    path(
        "plots/<uuid:subject_id>",
        login_required(PlotsView.as_view(), login_url="/login/",),
        name="plots",
    ),
    path(
        "session-queries/<uuid:subject_id>",
        SessionQueriesView.as_view(),
        name="session-queries",
    ),
    path(
        "sessions-load/<uuid:subject_id>",
        SessionsLoadView.as_view(),
        name="sessions-load",
    ),
    path(
        "tasks-load/<uuid:subject_id>",
        TasksLoadView.as_view(),
        name="tasks-load",
    ),
    path(
        "food-weight-plot/<uuid:subject_id>",
        login_required(FoodWeightView.as_view(), login_url="/login/",),
        name="food-weight-plot",
    ),
    path(
        "electrodelog-plot/<uuid:subject_id>",
        login_required(ElectrodeLogPlotView.as_view(), login_url="/login/",),
        name="electrodelog-plot",
    ),
    path(
        "task-plot/<uuid:subject_id>",
        login_required(TaskPlotView.as_view(), login_url="/login/",),
        name="task-plot",
    ),
    path(
        "electrode-status-plot/<uuid:subject_id>",
        login_required(ElectrodeStatusPlotView.as_view(), login_url="/login/",),
        name="electrode-status-plot",
    ),
    path(
        "subject-json/",
        login_required(getSubjectJson.as_view(), login_url="/login/",),
        name="subject-json",
    ),
]
