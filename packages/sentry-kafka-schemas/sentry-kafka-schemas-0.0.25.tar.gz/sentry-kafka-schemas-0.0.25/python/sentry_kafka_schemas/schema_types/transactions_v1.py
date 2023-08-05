from typing import Any, Dict, Literal, Union, TypedDict, List, Tuple
from typing_extensions import Required


class TransactionEvent(TypedDict, total=False):
    """transaction_event."""

    group_id: None
    group_ids: List[int]
    event_id: str
    organization_id: int
    project_id: int
    message: str
    platform: str
    datetime: str
    """format: date-time"""

    data: "_TransactionEventData"
    primary_hash: None
    retention_days: Union[int, None]
    occurrence_id: None
    occurrence_data: Dict[str, Any]
    is_new: bool
    is_regression: bool
    is_new_group_environment: bool
    queue: str
    skip_consume: bool
    group_states: None


_BaseAnyof0 = Union[str]
""" A "into-string" type that normalizes header names."""



class _TransactionEventData(TypedDict, total=False):
    event_id: Required[str]
    """Required property"""

    level: Required[str]
    """Required property"""

    version: Required[str]
    """Required property"""

    type: Required[str]
    """Required property"""

    transaction: Required[str]
    """Required property"""

    transaction_info: Required["_TransactionEventDataTransactionInfo"]
    """Required property"""

    logger: Required[str]
    """Required property"""

    platform: Required[str]
    """Required property"""

    timestamp: Required[Union[int, float]]
    """Required property"""

    start_timestamp: Required[Union[int, float]]
    """Required property"""

    received: Required[Union[int, float]]
    """Required property"""

    release: str
    environment: Required[str]
    """Required property"""

    contexts: Required["_TransactionEventDataContexts"]
    """Required property"""

    tags: Required[List[List[Union[None, str]]]]
    """Required property"""

    extra: "_TransactionEventDataExtra"
    sdk: Required["_TransactionEventDataSdk"]
    """Required property"""

    key_id: Required[str]
    """Required property"""

    project: Required[int]
    """Required property"""

    grouping_config: Required["_TransactionEventDataGroupingConfig"]
    """Required property"""

    spans: Required[List["_TransactionEventDataSpansItem"]]
    """Required property"""

    measurements: "_TransactionEventDataMeasurements"
    breakdowns: "_TransactionEventDataBreakdowns"
    _metrics: "_TransactionEventDataMetrics"
    span_grouping_config: Required["_TransactionEventDataSpanGroupingConfig"]
    """Required property"""

    culprit: Required[str]
    """Required property"""

    metadata: Required["_TransactionEventDataMetadata"]
    """Required property"""

    title: Required[str]
    """Required property"""

    location: Required[str]
    """Required property"""

    hashes: Required[List[str]]
    """Required property"""

    nodestore_insert: Required[Union[int, float]]
    """Required property"""



class _TransactionEventDataBreakdowns(TypedDict, total=False):
    span_ops: Required[Dict[str, "_TransactionEventDataMeasurementsNumOfSpans"]]
    """Required property"""



_TransactionEventDataContexts = Union[Dict[str, Union["_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0", None]]]
"""
 The Contexts Interface provides additional context data. Typically, this is data related to the
 current user and the environment. For example, the device or application version. Its canonical
 name is `contexts`.

 The `contexts` type can be used to define arbitrary contextual data on the event. It accepts an
 object of key/value pairs. The key is the “alias” of the context and can be freely chosen.
 However, as per policy, it should match the type of the context unless there are two values for
 a type. You can omit `type` if the key name is the type.

 Unknown data for the contexts is rendered as a key/value list.

 For more details about sending additional data with your event, see the [full documentation on
 Additional Data](https://docs.sentry.io/enriching-error-data/additional-data/).
"""



_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0 = Union["_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof0", "_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof1", "_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof2", "_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof3", "_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof4", "_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof5", "_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof6", "_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof7", "_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof8", "_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof9", "_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof10", "_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof11", Dict[str, Any]]
""" A context describes environment info (e.g. device, os or browser)."""



_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof0 = Union["_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof0Anyof0"]
"""
 Device information.

 Device context describes the device that caused the event. This is most appropriate for mobile
 applications.
"""



class _TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof0Anyof0(TypedDict, total=False):
    arch: Union[str, None]
    """ Native cpu architecture of the device."""

    battery_level: Union[Union[int, float], None]
    """
     Current battery level in %.

     If the device has a battery, this can be a floating point value defining the battery level
     (in the range 0-100).
    """

    battery_status: Union[str, None]
    """
     Status of the device's battery.

     For example, `Unknown`, `Charging`, `Discharging`, `NotCharging`, `Full`.
    """

    boot_time: Union[str, None]
    """ Indicator when the device was booted."""

    brand: Union[str, None]
    """ Brand of the device."""

    charging: Union[bool, None]
    """ Whether the device was charging or not."""

    cpu_description: Union[str, None]
    """
     CPU description.

     For example, Intel(R) Core(TM)2 Quad CPU Q6600 @ 2.40GHz.
    """

    device_type: Union[str, None]
    """
     Kind of device the application is running on.

     For example, `Unknown`, `Handheld`, `Console`, `Desktop`.
    """

    device_unique_identifier: Union[str, None]
    """ Unique device identifier."""

    external_free_storage: Union[int, None]
    """
     Free size of the attached external storage in bytes (eg: android SDK card).

    minimum: 0
    """

    external_storage_size: Union[int, None]
    """
     Total size of the attached external storage in bytes (eg: android SDK card).

    minimum: 0
    """

    family: Union[str, None]
    """
     Family of the device model.

     This is usually the common part of model names across generations. For instance, `iPhone`
     would be a reasonable family, so would be `Samsung Galaxy`.
    """

    free_memory: Union[int, None]
    """
     How much memory is still available in bytes.

    minimum: 0
    """

    free_storage: Union[int, None]
    """
     How much storage is free in bytes.

    minimum: 0
    """

    low_memory: Union[bool, None]
    """ Whether the device was low on memory."""

    manufacturer: Union[str, None]
    """ Manufacturer of the device."""

    memory_size: Union[int, None]
    """
     Total memory available in bytes.

    minimum: 0
    """

    model: Union[str, None]
    """
     Device model.

     This, for example, can be `Samsung Galaxy S3`.
    """

    model_id: Union[str, None]
    """
     Device model (internal identifier).

     An internal hardware revision to identify the device exactly.
    """

    name: Union[str, None]
    """ Name of the device."""

    online: Union[bool, None]
    """ Whether the device was online or not."""

    orientation: Union[str, None]
    """
     Current screen orientation.

     This can be a string `portrait` or `landscape` to define the orientation of a device.
    """

    processor_count: Union[int, None]
    """
     Number of "logical processors".

     For example, 8.

    minimum: 0
    """

    processor_frequency: Union[int, None]
    """
     Processor frequency in MHz.

     Note that the actual CPU frequency might vary depending on current load and
     power conditions, especially on low-powered devices like phones and laptops.

    minimum: 0
    """

    screen_density: Union[Union[int, float], None]
    """ Device screen density."""

    screen_dpi: Union[int, None]
    """
     Screen density as dots-per-inch.

    minimum: 0
    """

    screen_resolution: Union[str, None]
    """
     Device screen resolution.

     (e.g.: 800x600, 3040x1444)
    """

    simulator: Union[bool, None]
    """ Simulator/prod indicator."""

    storage_size: Union[int, None]
    """
     Total storage size of the device in bytes.

    minimum: 0
    """

    supports_accelerometer: Union[bool, None]
    """ Whether the accelerometer is available on the device."""

    supports_audio: Union[bool, None]
    """ Whether audio is available on the device."""

    supports_gyroscope: Union[bool, None]
    """ Whether the gyroscope is available on the device."""

    supports_location_service: Union[bool, None]
    """ Whether location support is available on the device."""

    supports_vibration: Union[bool, None]
    """ Whether vibration is available on the device."""

    timezone: Union[str, None]
    """ Timezone of the device."""

    usable_memory: Union[int, None]
    """
     How much memory is usable for the app in bytes.

    minimum: 0
    """



_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof1 = Union["_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof1Anyof0"]
"""
 Operating system information.

 OS context describes the operating system on which the event was created. In web contexts, this
 is the operating system of the browser (generally pulled from the User-Agent string).
"""



_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof10 = Union["_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof10Anyof0"]
"""
 OpenTelemetry Context

 If an event has this context, it was generated from an OpenTelemetry signal (trace, metric, log).
"""



class _TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof10Anyof0(TypedDict, total=False):
    attributes: Union[Dict[str, Any], None]
    """
     Attributes of the OpenTelemetry span that maps to a Sentry event.

     <https://github.com/open-telemetry/opentelemetry-proto/blob/724e427879e3d2bae2edc0218fff06e37b9eb46e/opentelemetry/proto/trace/v1/trace.proto#L174-L186>
    """

    resource: Union[Dict[str, Any], None]
    """
     Information about an OpenTelemetry resource.

     <https://github.com/open-telemetry/opentelemetry-proto/blob/724e427879e3d2bae2edc0218fff06e37b9eb46e/opentelemetry/proto/resource/v1/resource.proto>
    """



_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof11 = Union["_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof11Anyof0"]
"""
 Cloud Resource Context.

 This context describes the cloud resource the event originated from.

 Example:

 ```json
 "cloud_resource": {
     "cloud.account.id": "499517922981",
     "cloud.provider": "aws",
     "cloud.platform": "aws_ec2",
     "cloud.region": "us-east-1",
     "cloud.vavailability_zone": "us-east-1e",
     "host.id": "i-07d3301208fe0a55a",
     "host.type": "t2.large"
 }
 ```
"""



_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof11Anyof0 = TypedDict('_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof11Anyof0', {
    #  The cloud account ID the resource is assigned to.
    'cloud.account.id': Union[str, None],
    #  The zone where the resource is running.
    'cloud.availability_zone': Union[str, None],
    #  The cloud platform in use.
    #  The prefix of the service SHOULD match the one specified in cloud_provider.
    'cloud.platform': Union[str, None],
    #  Name of the cloud provider.
    'cloud.provider': Union[str, None],
    #  The geographical region the resource is running.
    'cloud.region': Union[str, None],
    #  Unique host ID.
    'host.id': Union[str, None],
    #  Machine type of the host.
    'host.type': Union[str, None],
}, total=False)


class _TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof1Anyof0(TypedDict, total=False):
    build: Union[str, None]
    """ Internal build number of the operating system."""

    kernel_version: Union[str, None]
    """
     Current kernel version.

     This is typically the entire output of the `uname` syscall.
    """

    name: Union[str, None]
    """ Name of the operating system."""

    raw_description: Union[str, None]
    """
     Unprocessed operating system info.

     An unprocessed description string obtained by the operating system. For some well-known
     runtimes, Sentry will attempt to parse `name` and `version` from this string, if they are
     not explicitly given.
    """

    rooted: Union[bool, None]
    """ Indicator if the OS is rooted (mobile mostly)."""

    version: Union[str, None]
    """ Version of the operating system."""



_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof2 = Union["_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof2Anyof0"]
"""
 Runtime information.

 Runtime context describes a runtime in more detail. Typically, this context is present in
 `contexts` multiple times if multiple runtimes are involved (for instance, if you have a
 JavaScript application running on top of JVM).
"""



class _TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof2Anyof0(TypedDict, total=False):
    build: Union[str, None]
    """ Application build string, if it is separate from the version."""

    name: Union[str, None]
    """ Runtime name."""

    raw_description: Union[str, None]
    """
     Unprocessed runtime info.

     An unprocessed description string obtained by the runtime. For some well-known runtimes,
     Sentry will attempt to parse `name` and `version` from this string, if they are not
     explicitly given.
    """

    version: Union[str, None]
    """ Runtime version string."""



_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof3 = Union["_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof3Anyof0"]
"""
 Application information.

 App context describes the application. As opposed to the runtime, this is the actual
 application that was running and carries metadata about the current session.
"""



class _TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof3Anyof0(TypedDict, total=False):
    app_build: Union[str, None]
    """ Internal build ID as it appears on the platform."""

    app_identifier: Union[str, None]
    """ Version-independent application identifier, often a dotted bundle ID."""

    app_memory: Union[int, None]
    """
     Amount of memory used by the application in bytes.

    minimum: 0
    """

    app_name: Union[str, None]
    """ Application name as it appears on the platform."""

    app_start_time: Union[str, None]
    """
     Start time of the app.

     Formatted UTC timestamp when the user started the application.
    """

    app_version: Union[str, None]
    """ Application version as it appears on the platform."""

    build_type: Union[str, None]
    """ String identifying the kind of build. For example, `testflight`."""

    device_app_hash: Union[str, None]
    """ Application-specific device identifier."""

    in_foreground: Union[bool, None]
    """ A flag indicating whether the app is in foreground or not. An app is in foreground when it's visible to the user."""



_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof4 = Union["_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof4Anyof0"]
""" Web browser information."""



class _TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof4Anyof0(TypedDict, total=False):
    name: Union[str, None]
    """ Display name of the browser application."""

    version: Union[str, None]
    """ Version string of the browser."""



_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof5 = Union["_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof5Anyof0"]
"""
 GPU information.

 Example:

 ```json
 "gpu": {
   "name": "AMD Radeon Pro 560",
   "vendor_name": "Apple",
   "memory_size": 4096,
   "api_type": "Metal",
   "multi_threaded_rendering": true,
   "version": "Metal",
   "npot_support": "Full"
 }
 ```
"""



class _TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof5Anyof0(TypedDict, total=False):
    api_type: Union[str, None]
    """
     The device low-level API type.

     Examples: `"Apple Metal"` or `"Direct3D11"`
    """

    graphics_shader_level: Union[str, None]
    """
     Approximate "shader capability" level of the graphics device.

     For Example: Shader Model 2.0, OpenGL ES 3.0, Metal / OpenGL ES 3.1, 27 (unknown)
    """

    id: Union[None, str]
    """ The PCI identifier of the graphics device."""

    max_texture_size: Union[int, None]
    """
     Largest size of a texture that is supported by the graphics hardware.

     For Example: 16384

    minimum: 0
    """

    memory_size: Union[int, None]
    """
     The total GPU memory available in Megabytes.

    minimum: 0
    """

    multi_threaded_rendering: Union[bool, None]
    """ Whether the GPU has multi-threaded rendering or not."""

    name: Union[str, None]
    """ The name of the graphics device."""

    npot_support: Union[str, None]
    """ The Non-Power-Of-Two support."""

    supports_compute_shaders: Union[bool, None]
    """ Whether compute shaders are available on the device."""

    supports_draw_call_instancing: Union[bool, None]
    """ Whether GPU draw call instancing is supported."""

    supports_geometry_shaders: Union[bool, None]
    """ Whether geometry shaders are available on the device."""

    supports_ray_tracing: Union[bool, None]
    """ Whether ray tracing is available on the device."""

    vendor_id: Union[str, None]
    """ The PCI vendor identifier of the graphics device."""

    vendor_name: Union[str, None]
    """ The vendor name as reported by the graphics device."""

    version: Union[str, None]
    """ The Version of the graphics device."""



_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof6 = Union["_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof6Anyof0"]
""" Trace context"""



class _TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof6Anyof0(TypedDict, total=False):
    client_sample_rate: Union[Union[int, float], None]
    """
     The client-side sample rate as reported in the envelope's `trace.sample_rate` header.

     The server takes this field from envelope headers and writes it back into the event. Clients
     should not ever send this value.
    """

    exclusive_time: Union[Union[int, float], None]
    """
     The amount of time in milliseconds spent in this transaction span,
     excluding its immediate child spans.
    """

    op: Union[str, None]
    """ Span type (see `OperationType` docs)."""

    parent_span_id: Union["_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof6Anyof0ParentSpanIdAnyof0", None]
    """ The ID of the span enclosing this span."""

    span_id: Required[Union["_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof6Anyof0ParentSpanIdAnyof0", None]]
    """
     The ID of the span.

    Required property
    """

    status: Union["_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof6Anyof0StatusAnyof0", None]
    """
     Whether the trace failed or succeeded. Currently only used to indicate status of individual
     transactions.
    """

    trace_id: Required[Union["_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof6Anyof0TraceIdAnyof0", None]]
    """
     The trace ID.

    Required property
    """



_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof6Anyof0ParentSpanIdAnyof0 = Union[str]
""" A 16-character hex string as described in the W3C trace context spec."""



_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof6Anyof0StatusAnyof0 = Union[Literal["ok"], Literal["cancelled"], Literal["unknown"], Literal["invalid_argument"], Literal["deadline_exceeded"], Literal["not_found"], Literal["already_exists"], Literal["permission_denied"], Literal["resource_exhausted"], Literal["failed_precondition"], Literal["aborted"], Literal["out_of_range"], Literal["unimplemented"], Literal["internal_error"], Literal["unavailable"], Literal["data_loss"], Literal["unauthenticated"]]
"""
Trace status.

Values from <https://github.com/open-telemetry/opentelemetry-specification/blob/8fb6c14e4709e75a9aaa64b0dbbdf02a6067682a/specification/api-tracing.md#status> Mapping to HTTP from <https://github.com/open-telemetry/opentelemetry-specification/blob/8fb6c14e4709e75a9aaa64b0dbbdf02a6067682a/specification/data-http.md#status>
"""
_TRANSACTIONEVENTDATACONTEXTSANYOF0ADDITIONALPROPERTIESANYOF0ANYOF6ANYOF0STATUSANYOF0_OK: Literal["ok"] = "ok"
"""The values for the 'Trace status' enum"""
_TRANSACTIONEVENTDATACONTEXTSANYOF0ADDITIONALPROPERTIESANYOF0ANYOF6ANYOF0STATUSANYOF0_CANCELLED: Literal["cancelled"] = "cancelled"
"""The values for the 'Trace status' enum"""
_TRANSACTIONEVENTDATACONTEXTSANYOF0ADDITIONALPROPERTIESANYOF0ANYOF6ANYOF0STATUSANYOF0_UNKNOWN: Literal["unknown"] = "unknown"
"""The values for the 'Trace status' enum"""
_TRANSACTIONEVENTDATACONTEXTSANYOF0ADDITIONALPROPERTIESANYOF0ANYOF6ANYOF0STATUSANYOF0_INVALID_ARGUMENT: Literal["invalid_argument"] = "invalid_argument"
"""The values for the 'Trace status' enum"""
_TRANSACTIONEVENTDATACONTEXTSANYOF0ADDITIONALPROPERTIESANYOF0ANYOF6ANYOF0STATUSANYOF0_DEADLINE_EXCEEDED: Literal["deadline_exceeded"] = "deadline_exceeded"
"""The values for the 'Trace status' enum"""
_TRANSACTIONEVENTDATACONTEXTSANYOF0ADDITIONALPROPERTIESANYOF0ANYOF6ANYOF0STATUSANYOF0_NOT_FOUND: Literal["not_found"] = "not_found"
"""The values for the 'Trace status' enum"""
_TRANSACTIONEVENTDATACONTEXTSANYOF0ADDITIONALPROPERTIESANYOF0ANYOF6ANYOF0STATUSANYOF0_ALREADY_EXISTS: Literal["already_exists"] = "already_exists"
"""The values for the 'Trace status' enum"""
_TRANSACTIONEVENTDATACONTEXTSANYOF0ADDITIONALPROPERTIESANYOF0ANYOF6ANYOF0STATUSANYOF0_PERMISSION_DENIED: Literal["permission_denied"] = "permission_denied"
"""The values for the 'Trace status' enum"""
_TRANSACTIONEVENTDATACONTEXTSANYOF0ADDITIONALPROPERTIESANYOF0ANYOF6ANYOF0STATUSANYOF0_RESOURCE_EXHAUSTED: Literal["resource_exhausted"] = "resource_exhausted"
"""The values for the 'Trace status' enum"""
_TRANSACTIONEVENTDATACONTEXTSANYOF0ADDITIONALPROPERTIESANYOF0ANYOF6ANYOF0STATUSANYOF0_FAILED_PRECONDITION: Literal["failed_precondition"] = "failed_precondition"
"""The values for the 'Trace status' enum"""
_TRANSACTIONEVENTDATACONTEXTSANYOF0ADDITIONALPROPERTIESANYOF0ANYOF6ANYOF0STATUSANYOF0_ABORTED: Literal["aborted"] = "aborted"
"""The values for the 'Trace status' enum"""
_TRANSACTIONEVENTDATACONTEXTSANYOF0ADDITIONALPROPERTIESANYOF0ANYOF6ANYOF0STATUSANYOF0_OUT_OF_RANGE: Literal["out_of_range"] = "out_of_range"
"""The values for the 'Trace status' enum"""
_TRANSACTIONEVENTDATACONTEXTSANYOF0ADDITIONALPROPERTIESANYOF0ANYOF6ANYOF0STATUSANYOF0_UNIMPLEMENTED: Literal["unimplemented"] = "unimplemented"
"""The values for the 'Trace status' enum"""
_TRANSACTIONEVENTDATACONTEXTSANYOF0ADDITIONALPROPERTIESANYOF0ANYOF6ANYOF0STATUSANYOF0_INTERNAL_ERROR: Literal["internal_error"] = "internal_error"
"""The values for the 'Trace status' enum"""
_TRANSACTIONEVENTDATACONTEXTSANYOF0ADDITIONALPROPERTIESANYOF0ANYOF6ANYOF0STATUSANYOF0_UNAVAILABLE: Literal["unavailable"] = "unavailable"
"""The values for the 'Trace status' enum"""
_TRANSACTIONEVENTDATACONTEXTSANYOF0ADDITIONALPROPERTIESANYOF0ANYOF6ANYOF0STATUSANYOF0_DATA_LOSS: Literal["data_loss"] = "data_loss"
"""The values for the 'Trace status' enum"""
_TRANSACTIONEVENTDATACONTEXTSANYOF0ADDITIONALPROPERTIESANYOF0ANYOF6ANYOF0STATUSANYOF0_UNAUTHENTICATED: Literal["unauthenticated"] = "unauthenticated"
"""The values for the 'Trace status' enum"""



_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof6Anyof0TraceIdAnyof0 = Union[str]
""" A 32-character hex string as described in the W3C trace context spec."""



_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof7 = Union["_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof7Anyof0"]
""" Profile context"""



class _TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof7Anyof0(TypedDict, total=False):
    profile_id: Required[Union["_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof7Anyof0ProfileIdAnyof0", None]]
    """
     The profile ID.

    Required property
    """



_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof7Anyof0ProfileIdAnyof0 = Union[str]
""" Wrapper around a UUID with slightly different formatting."""



_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof8 = Union[Dict[str, Any]]
""" Monitor information."""



_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof9 = Union["_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof9Anyof0"]
""" Response interface that contains information on a HTTP response related to the event."""



class _TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof9Anyof0(TypedDict, total=False):
    body_size: Union[int, None]
    """
     HTTP response body size.

    minimum: 0
    """

    cookies: Union["_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof9Anyof0CookiesAnyof0", None]
    """
     The cookie values.

     Can be given unparsed as string, as dictionary, or as a list of tuples.
    """

    headers: Union["_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof9Anyof0HeadersAnyof0", None]
    """
     A dictionary of submitted headers.

     If a header appears multiple times it, needs to be merged according to the HTTP standard
     for header merging. Header names are treated case-insensitively by Sentry.
    """

    status_code: Union[int, None]
    """
     HTTP status code.

    minimum: 0
    """



_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof9Anyof0CookiesAnyof0 = Union[Union[Dict[str, Union[str, None]], List["_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof9Anyof0CookiesAnyof0Anyof0Anyof1Item"]]]
""" A map holding cookies."""



_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof9Anyof0CookiesAnyof0Anyof0Anyof1Item = Union[Tuple[Union[str, None], Union[str, None]], None]
"""
maxItems: 2
minItems: 2
"""



_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof9Anyof0HeadersAnyof0 = Union[Union[Dict[str, Union["_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof9Anyof0HeadersAnyof0Anyof0Anyof0AdditionalpropertiesAnyof0", None]], List["_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof9Anyof0HeadersAnyof0Anyof0Anyof1Item"]]]
""" A map holding headers."""



_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof9Anyof0HeadersAnyof0Anyof0Anyof0AdditionalpropertiesAnyof0 = Union[str]
""" A "into-string" type that normalizes header values."""



_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof9Anyof0HeadersAnyof0Anyof0Anyof1Item = Union[Tuple[Union["_BaseAnyof0", None], Union["_TransactionEventDataContextsAnyof0AdditionalpropertiesAnyof0Anyof9Anyof0HeadersAnyof0Anyof0Anyof0AdditionalpropertiesAnyof0", None]], None]
"""
maxItems: 2
minItems: 2
"""



_TransactionEventDataExtra = Union[Dict[str, Any], None]
"""
 Arbitrary extra information set by the user.

 ```json
 {
     "extra": {
         "my_key": 1,
         "some_other_value": "foo bar"
     }
 }```
"""



class _TransactionEventDataGroupingConfig(TypedDict, total=False):
    enhancements: Required[str]
    """Required property"""

    id: Required[str]
    """Required property"""



class _TransactionEventDataMeasurements(TypedDict, total=False):
    num_of_spans: Required["_TransactionEventDataMeasurementsNumOfSpans"]
    """Required property"""



class _TransactionEventDataMeasurementsNumOfSpans(TypedDict, total=False):
    value: Required[Union[int, float]]
    """Required property"""

    unit: Required[str]
    """Required property"""



class _TransactionEventDataMetadata(TypedDict, total=False):
    title: Required[str]
    """Required property"""

    location: Required[str]
    """Required property"""



_TransactionEventDataMetrics = TypedDict('_TransactionEventDataMetrics', {
    # Required property
    'bytes.ingested.event': Required[int],
    # Required property
    'bytes.stored.event': Required[int],
}, total=False)


class _TransactionEventDataSdk(TypedDict, total=False):
    name: Required[str]
    """Required property"""

    version: Required[str]
    """Required property"""

    integrations: Required[List[str]]
    """Required property"""

    packages: Required[List["_TransactionEventDataSdkPackagesItem"]]
    """Required property"""



class _TransactionEventDataSdkPackagesItem(TypedDict, total=False):
    name: Required[str]
    """Required property"""

    version: Required[str]
    """Required property"""



class _TransactionEventDataSpanGroupingConfig(TypedDict, total=False):
    id: Required[str]
    """Required property"""



class _TransactionEventDataSpansItem(TypedDict, total=False):
    timestamp: Required[Union[int, float]]
    """Required property"""

    start_timestamp: Required[Union[int, float]]
    """Required property"""

    exclusive_time: Required[Union[int, float]]
    """Required property"""

    description: Required[str]
    """Required property"""

    op: Required[str]
    """Required property"""

    span_id: Required[str]
    """Required property"""

    parent_span_id: Required[str]
    """Required property"""

    trace_id: Required[str]
    """Required property"""

    same_process_as_parent: Required[Union[bool, None]]
    """Required property"""

    tags: Required[None]
    """Required property"""

    data: Required[None]
    """Required property"""

    hash: Required[str]
    """Required property"""



class _TransactionEventDataTransactionInfo(TypedDict, total=False):
    source: Required[str]
    """Required property"""

