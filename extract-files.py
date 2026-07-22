#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2016 The CyanogenMod Project
# SPDX-FileCopyrightText: 2017-2024 The LineageOS Project
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
    'vendor/samsung/m23xq',
    'vendor/qcom/opensource/dataservices',
    'vendor/qcom/opensource/display',
]

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
}

blob_fixups: blob_fixups_user_type = {
    'vendor/lib64/libsec-ril.so': blob_fixup()
        .binary_regex_replace(b'ril.dds.call.ongoing', b'vendor.calls.slot_id')
        .sig_replace(
            '60 0e 40 f9 82 0c 80 52 24 00 80 52 e1 03 15 aa 08 00 40 f9 e3 03 14 aa',
            '60 0e 40 f9 82 0c 80 52 24 00 80 52 e1 03 15 aa 08 00 40 f9 03 00 80 d2'
        ),
    (
        'vendor/lib64/hw/gatekeeper.mdfpp.so',
        'vendor/lib64/libskeymaster4device.so',
        'vendor/lib64/libkeymaster_helper.so',
        'vendor/lib/libwvhidl.so',
        'vendor/lib/mediadrm/libwvdrmengine.so',
    ): blob_fixup()
        .replace_needed('libcrypto.so', 'libcrypto-v33.so'),
    (
        'vendor/lib64/unihal_main@2.1.so',
        'vendor/lib64/libscaler_hw.unifunc.so',
        'vendor/lib/libscaler_hw.unifunc.so',
    ('vendor/lib64/nfc_nci_nxpsn.so'): blob_fixup()
        .add_needed('libbase_shim.so'),
    ): blob_fixup()
        .add_needed('libui_shim.so'),
    (
        'vendor/lib64/vendor.samsung.hardware.light-V1-ndk_platform.so',
        'vendor/bin/hw/vendor.samsung.hardware.light-service',
    ): blob_fixup()
        .replace_needed('android.hardware.light-V1-ndk_platform.so', 'android.hardware.light-V1-ndk.so'),
    'vendor/bin/hw/macloader': blob_fixup()
        .binary_regex_replace(b'vendor.wifi.dualconcurrent.interface', b'vnedor.wiff.dualconcurreut.iuterface')
        .binary_regex_replace(b'ro.vendor.wifi.sap.interface', b'ru.vnedor.wiff.sep.iuterface'),
    'vendor/lib64/libdpps.so': blob_fixup()
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so'),
    ('vendor/lib64/vendor.qti.hardware.camera.postproc@1.0-service-impl.so': blob_fixup()
        .sig_replace('9A 0A 00 94', '1F 20 03 D5'),
}  # fmt: skip

module = ExtractUtilsModule(
    'sm7225-common',
    'samsung',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
