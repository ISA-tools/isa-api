
from datetime import date
import json
import os
import shutil
# Make it work for Python 2+3 and with Unicode
import io


def main():
    blocks = []
    write_dir = "/Users/Philippe/Documents/git/isa-api/isatools/create/"
    data_header = str.join("\t", ("Accession Number", "calculated factor combinations", "counted factor combinations",
                                    "design automatic annotation", "number of sources", "number of samples",
                                    "curation warnings", "spurious factors"))

    fh = open(write_dir + "/" + str(date.today()) + "-MTBLS-ISA-curation-report.txt", "w")
    fh.writelines(data_header)
    fh.writelines("\n")

    with open('/Users/Philippe/Documents/PhenoMenal/Metabolights-metadata-Testing/out.txt') as fp:

        for line in fp:

            begin = False
            acc_num = 0
            # block = []
            if "load OK" in line:
                block = []
                start = line.strip()
                block.append(start)
                begin = True
                # print(begin)
                # print(line.strip())

            elif "load FAIL" in line:
                block = []
                start = line.strip()
                block.append(start)
                begin = True
                # print(begin)
                # print(line.strip())

            else:
                begin = False
                # print(line)
                # print(begin)
                block.append(line.strip())
            # print(block)
            if begin:
                blocks.append(block)

        # print(len(blocks))

    # print("BLOCK: ", blocks[3])

        data = []
    for e in blocks:
        # print("L: ",e)
        design = ""
        factors = {}
        factor_count = 0
        count_mat = {}
        spurious_factor = {}
        non_factors = []
        calc_nb_sg = -1

        for x in e:
            bits=[]
            if "load OK" in x:
                bits = x.split(" ")
                acc_num = bits[0]
                # print("acc_num: ", acc_num)

            elif "load FAIL" in x:
                bits = x.split(",")
                acc_num = bits[0]

                print("accnum: ", acc_num)
                max_nb_study_group = -1
                calc_nb_sg = -1
                design = "_"
                count_mat["source"] = "_"
                count_mat["sample"] = "_"
                sampling_event = bits[1]
                non_factors_as_string = "_"

            elif x.startswith("Calculated"):
                bits = x.split(" ")
                calc_nb_sg = int(bits[1])
                # print("number of calculated study groups: ", calc_nb_sg )

            elif x.startswith("Study sample level:"):
                bits = x.split(',')
                # print("group sizes: ", bits)
                for bit in bits:
                    bob_a, bob_b = bit.split(" = ")
                    if "total sources" in bob_a:
                        count_mat["source"] = int(bob_b)
                    if "total samples" in bob_a:
                        count_mat["sample"] = int(bob_b)

                    # print("check Source Definitions")
                if count_mat["source"] == count_mat["sample"]:
                    sampling_event = "single sampling"
                else:
                    # print("sample size: ", count_mat["source"], "| number of samples: ", count_mat["sample"])
                    sampling_event = "multiple/repeated samping"

            elif x.startswith("factor: "):
                bits = x.split("|")
                # print("BITS:", bits[1])
                factor_count = factor_count + 1
                bits[1] = bits[1].strip("' levels=")
                bits[1] = bits[1].strip(" '")
                # print("factor bits:", bits[1])
                if int(bits[1]) == 1:
                    spurious_factor[bits[0]] = int(bits[1])
                    # print("SPURIOUS FACTOR", bits[0], bits[1])
                    non_factors.append(bits[0])
                else:
                    factors[bits[0]] = int(bits[1])

            elif x.startswith("('"):
                bits = x.split(",")
                # print("treatment: ", bits)

        this_array = factors.values()
        max_nb_study_group = 1
        for element in this_array:
            # print("in array: ",element)
            max_nb_study_group = element * max_nb_study_group
        # print("max: ", max_nb_stdy_group)

        if count_mat["source"] == 1 and calc_nb_sg > 1:
            sampling_event = "ERROR LIKELY: check source declaration"
            # print(count_mat["source"], ":::", count_mat["sample"], "///",  calc_nb_sg)
            # print(sampling_event)

        if max_nb_study_group == calc_nb_sg:
            design = "full factorial  design"
            # print(design)

        elif max_nb_study_group > calc_nb_sg > 0:
            design = "fractional factorial design"
            # print(design)

        elif calc_nb_sg == -1:
            design = "none"

        # elif calc_nb_sg > 1 &

        else:
            print("problem with study group declaration, please review study!")

        non_factors_as_string = ';'.join(non_factors)
        print(acc_num, " \t ", max_nb_study_group, " \t ", calc_nb_sg, " \t ", design, " \t ", count_mat["source"], " \t ", count_mat["sample"], " \t ", sampling_event, " \t ", non_factors_as_string)

        data_element = {"study_key": acc_num,
                    "total_study_groups": max_nb_study_group,
                    "sources" : count_mat["source"],
                    "samples" : count_mat["sample"],
                    "inferred_study_design" :  design,
                    "sampling" : sampling_event,
                    "spurious_factors": non_factors_as_string}
        data.append(data_element)

        fh.writelines(str.join('\t', (acc_num, str(max_nb_study_group), str(calc_nb_sg), design, str(count_mat["source"]), str(count_mat["sample"]), sampling_event, non_factors_as_string)))
        fh.writelines("\n")

        try:
            to_unicode = unicode
        except NameError:
            to_unicode = str
        # Write JSON file
        with io.open('data.json', 'w', encoding='utf8') as outfile:
            str_ = json.dumps(data,
                              indent=4, sort_keys=True,
                              separators=(',', ': '), ensure_ascii=False)
            outfile.write(to_unicode(str_))


if __name__ == '__main__':
    main()