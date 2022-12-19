# This file is part of Streams.
#
# Streams is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# Streams is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Streams.  If not, see <https://www.gnu.org/licenses/>.

.PHONY: dist
dist:
	python -m build

.PHONY: upload
upload:
	python -m twine upload dist/*

.PHONY: upload-test
upload-test:
	python -m twine upload --repository testpypi dist/*