#
# MIT License
#
# Copyright © 2022 Hank AI, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""*magic* __path__ to support pkgutil namespace packages. This is a compromise
to fully adopting PEP420 implied namespace packaging. This is the most
compatible with Python v2 and v3. While Python v2 is EOL and should not be
a consideration, using PKGUTIL namespace packages is desireable since PEP420
does not currently have wide adoption in dev tools.

! IMPORTANT: Any and all projects using this namespace 'hankai' MUST use some
form of this __path__ manipulation with 'pkgutil'. If not, 'hankai' packages
will break.

https://packaging.python.org/guides/packaging-namespace-packages/
"""
__path__ = __import__("pkgutil").extend_path(__path__, __name__)
