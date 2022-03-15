#pragma once

#include "levenshtein.hpp"
#include "utils.hpp"

#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <regex>
#include <cmath>

template<typename F>
F trunc_decs(const F& f,
             int decs)
{
    int i1 = floor(f);
    F rmnd = f - i1;
    int i2 = static_cast<int> (rmnd * std::pow(10, decs));
    F f1 = i2 / std::pow(10, decs);

    return i1 + f1;
}


double cer_on_text(const std::string& org_file_path, const std::string& ocr_file_path) {
    std::string org_line = readFile2(org_file_path);
    std::string ocr_line = readFile2(ocr_file_path);

    org_line.erase(remove(org_line.begin(), org_line.end(), '\n'), org_line.end());
    ocr_line.erase(remove(ocr_line.begin(), ocr_line.end(), '\n'), ocr_line.end());

    org_line.erase(remove(org_line.begin(), org_line.end(), ' '), org_line.end());
    ocr_line.erase(remove(ocr_line.begin(), ocr_line.end(), ' '), ocr_line.end());

    return trunc_decs(levenshtein_distance(org_line.c_str(), org_line.size(), ocr_line.c_str(), ocr_line.size()) / org_line.size() * 100, 2);
}