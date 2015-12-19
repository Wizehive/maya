import os, fnmatch
from wg_config import source_path
from wg_config import canonical_build_path

class PluginCanonicalCodeBuilder:

	def __init__(self, source_path, build_path):
		self.source_path = source_path
		self.build_path = build_path

	def build(self, context):
		self.plugin_name = context['plugin_name']

		self.plugin_path = self.source_path + '/' + self.plugin_name
		self.dependencies_path = self.source_path + '/common'
		self.plugin_dependencies_config_path = self.plugin_path + '/dependencies'
		self.plugin_register_file_path = self.plugin_path + '/plugin-register.js'
		self.plugin_build_path = self.build_path + '/' + self.plugin_name

		self.create_plugin_build_path()
		self.merge_files_into_one('js')
		self.merge_files_into_one('html')
		self.merge_files_into_one('css')

	def create_plugin_build_path(self):
		if not os.path.exists(self.plugin_build_path):
			os.makedirs(self.plugin_build_path)

	def merge_files_into_one(self, extension):
		target_file_path = self.create_target_file(extension)

		self.merge_plugin_files(extension, target_file_path)
		self.merge_dependency_files(extension, target_file_path)

		if extension == 'js':
			self.append_plugin_register(target_file_path)

	def create_target_file(self, extension):
		target_file_name = 'plugin.' + extension
		target_file_path = self.plugin_build_path + '/' + target_file_name
		open(target_file_path, 'w').close()
		return target_file_path

	def merge_plugin_files(self, extension, target_file_path):
		self.merge_all_files_with_extension(self.plugin_path, extension, target_file_path)

	def merge_dependency_files(self, extension, target_file_path):
		with open(self.plugin_dependencies_config_path) as f:

			dependencies = f.read().splitlines()

			for dependency in dependencies:
				dependency_path = self.dependencies_path + '/' + dependency
				self.merge_all_files_with_extension(dependency_path, extension, target_file_path)

	def merge_all_files_with_extension(self, module_path, extension, target_file_path):
		path = module_path + '/src'

		files_with_extension = self.get_files_with_extension(path, extension)

		if files_with_extension:
			self.append_content_of_files(files_with_extension, target_file_path)

	def get_files_with_extension(self, path, extension):
		files_with_extension = []

		for root, dirnames, filenames in os.walk(path):
			for filename in fnmatch.filter(filenames, '*.' + extension):
				files_with_extension.append(os.path.join(root, filename))

		return files_with_extension

	def append_content_of_files(self, source_file_names, target_file_path):
		with open(target_file_path, 'a') as target_file:
			for source_file_name in source_file_names:
				with open(source_file_name) as source_file:
					for line in source_file:
						target_file.write(line)
					target_file.write('\n')

	def append_plugin_register(self, target_file_path):
		plugin_register_file = open(self.plugin_register_file_path)
		f = open(target_file_path, 'a')
		f.write(plugin_register_file.read())

def make_canonical_builder():
	return PluginCanonicalCodeBuilder(source_path, canonical_build_path)
