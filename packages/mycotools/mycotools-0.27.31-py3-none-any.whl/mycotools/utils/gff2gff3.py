#! /usr/bin/env python3

# NEED to arrive at a consensus for protein and transcript IDs

import re
import sys
import argparse
from mycotools.lib.biotools import gff2list, list2gff, gff2Comps, gff3Comps
from mycotools.lib.kontools import format_path, eprint, vprint
from mycotools.utils.gtf2gff3 import add_genes, remove_start_stop

def gff2gff3(gff_list, ome, jgi_ome):

    comps2, exon_dict, cds_dict, out_list, gene_dict = gff2Comps(), {}, {}, [], {}
    for entry in gff_list:
        if entry['type'] == 'exon':
            name = re.search( comps2['id'], entry['attributes'] )[1]
  #          try:
            transcript = re.search( comps2['transcript'], entry['attributes'] )[1]
  
  #except TypeError:
 #               print(entry['attributes'], comps2['transcript'], flush = True)
#                sys.exit()
            if name not in exon_dict:
                exon_dict[name] = 0
            if name not in gene_dict:
                gene_dict[name] = { 
                    'protein': '', 'transcript': '', 'product': ''
                    }
            gene_dict[name]['transcript'] = transcript
            exon_dict[name] += 1
            exon_id = 'ID=exon_' + transcript + '_' + str(exon_dict[name])
            par_id = 'mRNA_' + transcript
            entry['attributes'] = exon_id + ';Parent=' + par_id + ';Alias=' + name
        elif entry['type'] == 'CDS':
            name = re.search( comps2['id'], entry['attributes'] )[1]
            protein = re.search( comps2['prot'], entry['attributes'] )[1]
            product = re.search( comps2['product'], entry['attributes'] )
            if name not in cds_dict:
                cds_dict[name] = 0
            if name not in gene_dict:
                gene_dict[name] = { 
                    'protein': '', 'transcript': '', 'product': ''
                    }
            if product is not None:
                gene_dict[name]['product'] = product[1]
            gene_dict[name]['protein'] = protein
            cds_dict[name] += 1
            cds_id = 'CDS_$_' + str( cds_dict[name] )
            entry['attributes'] = 'ID=' + cds_id + ';Alias=' + name

    comps3 = gff3Comps()
    for entry in gff_list:
        if entry['type'] not in {'start_codon', 'stop_codon'}:
            if entry['type'] == 'exon':
                name = re.search( comps3['Alias'], entry['attributes'] )[1]
                trans = gene_dict[name]['transcript']
                prot = ome + '_' + gene_dict[name]['protein']
                entry['attributes'] = re.sub(
                    comps3['Alias'], 
                    'Parent=mRNA_' + trans + ';Alias=' + prot, 
                    entry['attributes']
                    )
            elif entry['type'] == 'CDS':
                name = re.search( comps3['Alias'], entry['attributes'] )[1]
                trans = gene_dict[name]['transcript']
                prot = ome + '_' + gene_dict[name]['protein']
                entry['attributes'] = re.sub(
                    r'ID=CDS_\$_(\d+)', 
                    'ID=CDS_' + trans + r'_\1;' + 'Parent=mRNA_' + trans,
                    entry['attributes']
                    )
                entry['attributes'] = re.sub(
                    comps3['Alias'], 'Alias=' + prot, entry['attributes']
                    )
            elif entry['type'] == 'gene':
                name = re.search( comps2['id'], entry['attributes'] )[1]
                gene = 'gene_' + gene_dict[name]['transcript']
                prot = gene_dict[name]['protein']
                jgi = 'jgi.p|' + jgi_ome + '|' + prot
                prod = gene_dict[name]['product']
                trans = gene_dict[name]['transcript']
                alias = ome + '_' + prot
                entry['attributes'] = 'ID=' + gene + ';Name=' + jgi + \
                    ';portal_id=' + jgi_ome + ';product_name=' + prod + \
                    ';proteinId=' + prot + ';transcriptId=' + trans + \
                    ';Alias=' + alias
            elif entry['type'] == 'mRNA':
                name = re.search( comps2['id'], entry['attributes'] )[1]
                gene = 'gene_' + gene_dict[name]['transcript']
                mrna = 'mRNA_' + gene_dict[name]['transcript']
                prot = gene_dict[name]['protein']
                jgi = 'jgi.p|' + jgi_ome + '|' + prot
                trans = gene_dict[name]['transcript']
                alias = ome + '_' + prot
                entry['attributes'] = 'ID=' + mrna + ';Name=' + jgi + \
                    ';Parent=' + gene + \
                    ';proteinId=' + prot + ';transcriptId=' + trans + \
                    ';Alias=' + alias
            out_list.append( entry )

    return out_list


def main(gff_list, ome, jgi_ome, safe = True, verbose = True):

    gff_prep, failed, flagged = add_genes( gff_list, safe = safe )
    if failed:
        vprint( str(len(failed)) + '\tgenes failed', v = verbose , e = True, flush = True)
    if flagged:
        vprint( str(len(flagged)) + '\tgene coordinates from exons', v = verbose, e = True, flush = True)
    gff3 = gff2gff3(gff_prep, ome, jgi_ome)

    return gff3

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser( description = 'Converts jgi gff2 to gff3' )
    parser.add_argument( '-i', '--input', required = True, help = 'JGI gff2' )
    parser.add_argument( '-o', '--ome', required = True, help = 'Internal ome' )
    parser.add_argument( '-j', '--jgi', required = True, help = 'JGI ome' )
    parser.add_argument( '--fail', default = True, action = 'store_false', \
        help = 'Fail genes w/o CDS sequences that lack start or stop codons' )
    args = parser.parse_args()

    gff_list = gff2list(format_path( args.input ))
    eprint( args.ome + '\t' + args.input , flush = True)
    gff3 = main( gff_list, args.ome, args.jgi, args.fail )
    print( list2gff( gff3 ) , flush = True)

    sys.exit( 0 )
