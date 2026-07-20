#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: The Infinity-X Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/samsung/sm7225-common',
    'hardware/qcom-caf/sm8250',
    'hardware/qcom-caf/wlan',
    'hardware/samsung',
    'vendor/qcom/opensource/dataservices',
    'vendor/qcom/opensource/display',
]

blob_fixups: blob_fixups_user_type = {
    # Display / Scaler
    (
        'vendor/lib64/unihal_main@2.1.so',
        'vendor/lib64/libscaler_hw.unifunc.so',
        'vendor/lib/libscaler_hw.unifunc.so',
    ): blob_fixup()
        .add_needed('libui_shim.so'),
    # DPPS
    'vendor/lib64/libdpps.so': blob_fixup()
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so'),
    # Keymaster / Gatekeeper / DRM
    (
        'vendor/lib64/hw/gatekeeper.mdfpp.so',
        'vendor/lib64/libskeymaster4device.so',
        'vendor/lib64/libkeymaster_helper.so',
        'vendor/lib/libwvhidl.so',
        'vendor/lib/mediadrm/libwvdrmengine.so',
    ): blob_fixup()
        .replace_needed('libcrypto.so', 'libcrypto-v33.so'),
    # Lights
    (
        'vendor/lib64/vendor.samsung.hardware.light-V1-ndk_platform.so',
        'vendor/bin/hw/vendor.samsung.hardware.light-service',
    ): blob_fixup()
        .replace_needed('android.hardware.light-V1-ndk_platform.so', 'android.hardware.light-V1-ndk.so'),
    # RIL
    'vendor/lib64/libsec-ril.so': blob_fixup()
        .binary_regex_replace(b'ril.dds.call.ongoing', b'vendor.calls.ongoing'),
    # Wi-Fi
    'vendor/bin/hw/macloader': blob_fixup()
        .binary_regex_replace(b'vendor.wifi.dualconcurrent.interface', b'vnedor.wiff.dualconcurreut.iuterface')
        .binary_regex_replace(b'ro.vendor.wifi.sap.interface', b'ru.vnedor.wiff.sep.iuterface'),
}  # fmt: skip

module = ExtractUtilsModule(
    'sm7225-common',
    'samsung',
    namespace_imports=namespace_imports,
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
