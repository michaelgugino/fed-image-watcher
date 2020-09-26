# -*- coding: utf-8 -*-
# This file is part of fedimg.
# Copyright (C) 2014-2018 Red Hat, Inc.
#
# fedimg is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# fedimg is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with fedimg; if not, see http://www.gnu.org/licenses,
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
# Authors:  David Gay <dgay@redhat.com>
#           Sayan Chowdhury <sayanchowdhury@fedoraproject.org>

def process_compose(self, location, compose_id):
    try:
        compose_metadata = fedfind.release.get_release(
            cid=compose_id).metadata
    except fedfind.exceptions.UnsupportedComposeError:
        _log.debug("%r is unsupported compose" % compose_id)
        return

    images_meta = []
    for arch in ['x86_64', 'aarch64']:
        cloud_meta = get_value_from_dict(
            compose_metadata, 'images', 'payload', 'images',
            'Cloud', arch)
        atomic_meta = get_value_from_dict(
            compose_metadata, 'images', 'payload',
            'images', 'AtomicHost', arch)

        if cloud_meta:
            images_meta.extend(cloud_meta)
        if atomic_meta:
            images_meta.extend(atomic_meta)

    if not images_meta:
        _log.debug('No compatible image found to process')
        return

    upload_urls = get_rawxz_urls(location, images_meta)
    if len(upload_urls) > 0:
        _log.info("Start processing compose id: %s", compose_id)
        fedimg.uploader.upload(
            pool=self.upload_pool,
            urls=upload_urls,
            compose_id=compose_id,
            push_notifications=True
        )

def upload(pool, urls, *args, **kwargs):
    """
    Takes a list (urls) of one or more .raw.xz image files and
    sends them off to cloud services for registration. The upload
    jobs threadpool must be passed as `pool`.

    Args:
        pool (multithreading.pool.ThreadPool): The thread pool to parallelize
        the uploads.
        urls (list): List of cloud image urls.
    """

    active_services = ACTIVE_SERVICES
    compose_id = kwargs.get('compose_id')
    push_notifications = kwargs.get('push_notifications')

    if 'aws' in active_services:
        _log.info('Starting to process AWS EC2Service.')
        images_metadata = ec2main(
            urls,
            AWS_ACCESS_ID,
            AWS_SECRET_KEY,
            [AWS_BASE_REGION],
            compose_id=compose_id,
            push_notifications=push_notifications,
        )
        for image_metadata in images_metadata:
            image_id = image_metadata['image_id']
            aws_regions = list(set(AWS_REGIONS) - set([AWS_BASE_REGION]))
            ec2copy(
                aws_regions,
                AWS_ACCESS_ID,
                AWS_SECRET_KEY,
                image_ids=[image_id],
                push_notifications=push_notifications,
                compose_id=compose_id
            )
        _log.info('AWS EC2Service process is completed.')
