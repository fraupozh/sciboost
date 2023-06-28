# Sciboost


The tool assists in searching medical databases for adverse effects reported in the literature.
This project is specifically for the LMU Klinikum Laboratory, which focuses on identifying and addressing therapeutic resistance in gastrointestinal cancers to personalize drug selection.

A fine-tuned SciBERT model for the task of identifying drug-adverse effect entities through Named Entity Recognition (NER) is used as a core of the tool (1).
The entities will be mapped to MedDRA, and alongside the identified entities, various study characteristics will be visualized for users.

1. [Fine-Tuning SciBERT to Recognize Drug Names and Adverse Effects, JUSTIN SEONYONG LEE, 2021](http://www.columbia.edu/~jsl2239/adverse_effects_ner.html)

# Sciboost Functionality

This project uses MetaMap, a software provided by the U.S. National Library of Medicine (NLM), as part of its functionality.

## MetaMap Usage Notice

The usage of MetaMap and MetaMap Tools in this project is subject to the following conditions:

- Redistributions of source code must retain this Informational Notice.
- Redistributions in binary form must reproduce this Informational Notice, this list of conditions, and the following disclaimer in the documentation and/or other materials provided with the distribution.
- Neither the names of the National Library of Medicine, the National Institutes of Health, nor the names of any of the software developers may be used to endorse or promote products derived from this software without specific prior written permission.
- The U.S. Government retains an unlimited, royalty-free right to use, distribute, or modify the software.

Please acknowledge NLM as the source of the MetaMap software by including the phrase "Courtesy of the U.S. National Library of Medicine" or "Source: U.S. National Library of Medicine."

THIS SOFTWARE IS PROVIDED BY THE U.S. GOVERNMENT AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE U.S. GOVERNMENT OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

For more information about MetaMap, visit the [MetaMap website](https://metamap.nlm.nih.gov/).

