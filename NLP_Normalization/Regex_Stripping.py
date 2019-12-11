# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 23:06:05 2017

@author: kach
"""

import re

txt='''Thanks Vandana for highlighting, Can you confirm if traveller came back to you confirming Amex cant match it finally despite raising it with them? I will anyway meanwhile raise it with Amex. Regards, Gaurav 
From:  mstravel  Sent:  03 September 2014 07:54 To:  Gaurav Kukreja (Brook Street) Subject:  CAS-19525-F5M6H0 | FW: Flight Cost Hi Gaurav, We require your help in investigating this with Amex Cyprus for not able to match the  fare offered by other online engine. Julia has asked us to let you know on this example -difference of fare between Amex and outside vendor. Thanks, Vandana 
From:  Julia Fidler  Sent:      Tuesday, September 2, 2014 3:23 PM To:  Daris Hechevarria Cc:  Daniel Nevado; mstravel Subject:  RE: Flight Cost Hi Daris     We do have a low fare guarantee with Amex, although there are some exceptions (eg leisure fares), would you be able to share     the below with the travel agency and ask that they match it, if they are unable to please send their written response to      mstravel@miscrosoft.com Many thanks! 
From:  Daris Hechevarria  Sent:  02 September 2014 12:00 To:  Julia Fidler Cc:  Daniel     Nevado Subject:  Flight Cost Hi Julia, My manager suggested I reach out to you concerning the flight cost differential between     the quoted Amex price of a flight and the internet price.  Is there something we can manage to ensure closer parity?  We would     like to continue using Amex as the primary booking engine and avoid shifting to personal expensing on this. '''

#cleantxt=re.sub('From:.*?Subject:','',txt,flags=re.DOTALL)
cleantxt=re.sub('From:.*?To:.*?Subject:','',txt,flags=re.DOTALL)
print(cleantxt)
