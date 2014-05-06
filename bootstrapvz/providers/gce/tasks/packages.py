from bootstrapvz.base import Task
from bootstrapvz.common import phases
from bootstrapvz.common.tasks import apt
from bootstrapvz.common.tools import log_check_call
import os
import os.path


class DefaultPackages(Task):
	description = 'Adding image packages required for GCE'
	phase = phases.preparation
	predecessors = [apt.AddDefaultSources]

	@classmethod
	def run(cls, info):
		info.packages.add('python')
		info.packages.add('sudo')
		info.packages.add('ntp')
		info.packages.add('lsb-release')
		info.packages.add('acpi-support-base')
		info.packages.add('openssh-client')
		info.packages.add('openssh-server')
		info.packages.add('dhcpd')

		kernel_packages_path = os.path.join(os.path.dirname(__file__), '../../ec2/tasks/packages-kernels.json')
		from bootstrapvz.common.tools import config_get
		kernel_package = config_get(kernel_packages_path, [info.release_codename,
		                                                   info.manifest.system['architecture']])
		info.packages.add(kernel_package)


class GooglePackages(Task):
	description = 'Adding image packages required for GCE from Google repositories'
	phase = phases.preparation
	predecessors = [DefaultPackages]

	@classmethod
	def run(cls, info):
		info.packages.add('google-compute-daemon')
		info.packages.add('google-startup-scripts')
		info.packages.add('python-gcimagebundle')


class InstallCloudSDK(Task):
	description = 'Install Cloud SDK, not yet packaged'
	phase = phases.package_installation

	@classmethod
	def run(cls, info):
		cloudsdk_directory = os.path.join(info.root, 'usr/local/share/google')
		gsutil_binary = os.path.join(os.path.join(info.root, 'usr/local/bin'), 'gsutil')
		gcutil_binary = os.path.join(os.path.join(info.root, 'usr/local/bin'), 'gcutil')
		gcompute_binary = os.path.join(os.path.join(info.root, 'usr/local/bin'), 'gcompute')
		log_check_call(['wget', 'https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk-coretools-linux-x86_64.tar.gz'])
		os.makedirs(cloudsdk_directory)
		log_check_call(['tar', 'xaf', 'google-cloud-sdk-coretools-linux-x86_64.tar.gz', '-C', cloudsdk_directory])
		log_check_call(['ln', '-s', '../share/google/google-cloud-sdk/bin/gsutil', gsutil_binary])
		log_check_call(['ln', '-s', '../share/google/google-cloud-sdk/bin/gcutil', gcutil_binary])
		log_check_call(['ln', '-s', '../share/google/google-cloud-sdk/bin/gcompute', gcompute_binary])
