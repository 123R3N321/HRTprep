'''
This is probably the ONE leetcode question I will tackle in the prep repo,
as it has been made clear that HRT views leetcode-styled questions
"too-much of hit or miss" situation.

However, I am presenting a solution not widely adapted in this leetcode discussion
'''

'''
You might want to say 'wtf' at first glance at the re pattern here, but hear me out
it can be analyzed layer by layer:
1. it consists of r'...|...' where, first part will be priority matched, and it is the "//"
pattern: consider this case: "//blah blah /* blah ..." where the /* pattern is not meaningful

2. [^n]* pattern, which means "match against any number of places of anything that is not
a newline char", pattern matching stops at newline char

3. the S and s pattern allows anything, including newline char, to be matched

4. [...]*? is lazy matching, matches for shortest pattern
(in other words, we need lazy matching because S s matching is too powerful) 
'''
def removeCommentsRe(lst):
    raw = '\n'.join(lst)    # re-construct the entire raw text, delimited by whitespace

    import re
    pattern = re.compile(r'\/\/[^\n]*|\/\*[\S\s]*?\*\/')
    cleaned = pattern.sub('',raw)
    res = cleaned.split('\n')
    emptyRemoved = []
    for each in res:
        if len(each)>0:
            emptyRemoved.append(each)
    return emptyRemoved

if __name__ == '__main__':
    raw = [
        "/* this is sample code 8*/",
        "int main() { //simply main func",
        "std::cout<<'x'<<std::endl;/* simple print",
        "looks messy in c/c++ sigh... */return 0;",
        "}//we done"
    ]
    for each in removeCommentsRe(raw):
        print(each)