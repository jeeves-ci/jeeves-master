# import boto
# import os
#
# AWS_ACCESS_KEY_ID = "AKIAJYKLSPUXP73WDNDA"
# AWS_SECRET_ACCESS_KEY = "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"
#
# def download_from_s3(s3_url, dst_path):
#     """
#     Download a file from S3 to a given path
#     """
#     if os.path.isfile(dst_path):
#         raise RuntimeError('Local destination path \'{}\' already exists'
#                            .format(dst_path))
#
#     conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
#                            AWS_SECRET_ACCESS_KEY)
#     bucket_name = os.path.basename(os.path.dirname(s3_url))
#     resource_name = os.path.basename(s3_url)
#
#     print 'getting bucket with name {}'.format(bucket_name)
#     bucket = conn.get_bucket(bucket_name)
#     print 'getting resource {} from bucket'.format(resource_name)
#     resource = bucket.get_key(resource_name)
#     print 'Downloading resource to {}'.format(dst_path)
#     resource.get_contents_to_filename(dst_path)
#
#
# download_from_s3("s3://singular-exercise/report.csv", "report.csv")

# import pandas as pd
#
# report_file = 'report.csv'
# report_data = pd.read_csv(report_file)
# report_lines = report_data.splitlines()

a = [1, 2, 3, 4, 5]
print a[1:]
for i in xrange(0, len(a)):
    for e in xrange(i + 1, len(a)):
        print 'i ' + str(i)
        print 'e ' + str(e)

# import pandas as pd
# pd.Series.from_csv()
#
# dfs = pd.read_csv('group_data.csv')
# dfs.irow(1)
