'''To map the extracted ADEs to MedDRA PTs, we processed the text through MetaMap,
 which assigns Concept Unique Identifiers (CUIs) from the Unified Medical Language System (UMLS)
   to biomedical text. From the UMLS CUI, we identify 
   the MedDRA PT associated with that CUI.
     If one exists, we assign the MedDRA PT to the mention.'''


import argparse
import os
from skr_web_api import Submission, METAMAP_INTERACTIVE_URL

""" MetaMap interactive using embedded string """

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="test cas auth")
    parser.add_argument('-s', '--serviceurl',
                        default=METAMAP_INTERACTIVE_URL,
                        help='url of service')
    parser.add_argument('-e', '--email', help='Email address')
    parser.add_argument('-a', '--apikey', help='UTS api key')
    args = parser.parse_args()

    email = args.email or os.getenv('UTS_EMAIL')
    api_key = args.apikey or os.getenv('UTS_API_KEY')

    inputtext = "A spinal tap was performed and oligoclonal bands were \
detected in the cerebrospinal fluid.\n"

    inst = Submission(email, api_key)
    if args.serviceurl:
        inst.set_serviceurl(args.serviceurl)

    inst.init_mm_interactive(inputtext, args='-N')
    response = inst.submit()

    print('response status: {}'.format(response.status_code))
    print('content: {}'.format(response.content.decode()))
