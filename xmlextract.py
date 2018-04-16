#!/usr/bin/env python

from commandline import CMDBuilder,cmdbuild
import os, logging
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)

@CMDBuilder.cmdbuild('extract')
class XmlExtracter(object):
    def __init__(self):
        pass

    @CMDBuilder.Args('ifile', help='Input file')
    @CMDBuilder.Args('ofile', default='.', help='output file')
    @CMDBuilder.Args('-b', '--xbegins',nargs="+", default=['?xml'], help='being of the xml string')
    @CMDBuilder.Args('-e', '--xends', nargs="+" , default=['svc_init','svc_result'], help='end of the xml string')
    def ext(self, ifile, ofile, xbegins, xends):
        xbegins = ['<%s' % begin for begin in xbegins]
        xends = ["</%s>" % end for end in xends]
        if not os.path.exists(ifile):
            logger.error('%s is not exists!' % ifile)
            return
        xmlstart = False
        xmldata = []
        with open(ifile, 'r') as f:
            count = 1
            for l in f.readlines():
                l = l.strip()
                if l in xbegins:
                    #
                    xmlstart = True
                    xmldata.append(l.strip())
                    continue
                if not xmlstart:
                    continue

                xmldata.append(l)
                if l in xends:
                    xmlstart = False
                    # output to file
                    print('writ %s_%s file' % (ofile, count))
                    with open("%s_%s"% (ofile, count),'w') as of:
                        of.writelines('\n'.join(xmldata))
                    count += 1
                    xmldata=[]

    @CMDBuilder.Args('ifiles', nargs="+", help='Input file')
    def parse(self, ifiles):
        for f in ifiles:
            if not os.path.exists(f):
                print('ERROR %s not found !' % f)
                continue
            print('Parse %s' % f)
            tree = ET.parse(f)
            root = tree.getroot()
            self._traverseXml(root)

    def _traverseXml(self, element):
        if len(element)>0:
            for child in element:
                print (child.tag, "----", child.attrib, child.text)
                self._traverseXml(child)

if __name__ == "__main__":
    CMDBuilder.run()
