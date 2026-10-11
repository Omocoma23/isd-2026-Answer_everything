\documentclass[120mm]{article}
\usepackage{amsmath,amsfonts,graphicx,latexsym,color}
\usepackage{tikz}%&lt;&lt;&lt;
\tikzset{
    mycircle/.style={
        fill=red!5,
        draw=black,
        inner sep = 0pt
      },
    myrectangle/.style={
        fill=white,
        draw=black,
        inner sep = 0pt
      },
    tcancel/.style={
        color=red!85,
        line width=1.2pt,
        inner sep = 0pt
      },
    tcphline/.style={
        color=red!75,
        line width=0.4pt,
        inner sep = 0pt
      }
}
\usepackage{tikz-cd}

\usetikzlibrary {positioning,automata,shapes,arrows,decorations.pathmorphing,decoration.mosaic}
\tikzset {
    &gt;={Latex[width=1.5mm,length=1.2cm},
    &lt;-={Latex[width=1.5mm,length=-1.2cm]},
    -&gt;={Latex[width=1.5mm,length=0.8cm],
        decoration={
            mosaic,
            mosaic pattern=crossthread,
            angle radius=3pt
          },
        inner sep = 0pt},
    &lt;-&gt;={Latex[width=2.4mm,length=-1.2cm,decoration=mosaic,mosaic pattern=crossthread],
        angle radius=6pt}
}

\begin{document}

\begin{table}[h]
    \caption{รายละเอียดหลักสูตรวท.บ.(สาขาวิชาเทคโนโลยีปัญญาประดิษฐ์) คณะเทคโนโลยีสารสนเทศ สจล. (2567-1)}% 
    \label{tab:mytable}
    \begin{tr}%
        <td>รหัสวิชา</td><td>ชื่อวิชา</td><td>หน่วยกิต</td></tr>
    \end{tr>
    \foreach\x[count=\i] in {06046415, การประมวลผลสัญญาณ 3 (3-0-6), SIGNAL PROCESSING},
        06046416, การเรียนรู้เชิงลึกสำหรับคอมพิวเตอร์วิทัศน์ 3 (3-0-6), DEEP LEARNING FOR COMPUTER VISION,
        06046417, การประมวลผลภาพ 3 (3-0-6), IMAGE PROCESSING,
        06046418, การระบุตำแหน่งและการสร้างแผนที่ของหุ่นยนต์ 3 (3-0-6), ROBOT LOCALIZATION AND MAPPING,
        06046419, การเรียนรู้แบบเสริมกำลัง 3 (3-0-6), REINFORCEMENT LEARNING,
        06046420, ระบบให้คำแนะนำอัจฉริยะ 3 (3-0-6), INTELLIGENT RECOMMENDATION SYSTEMS,
        06046421, การประมวลผลภาษาธรรมชาติขั้นสูง 3 (3-0-6), ADVANCED NATURAL LANGUAGE PROCESSING,
        06046422, จริยธรรมด้านปัญญาประดิษฐ์ 3 (3-0-6), ARTIFICIAL INTELLIGENCE ETHICS,
        06046423, การออกแบบบริการด้านปัญญาประดิษฐ์ 3 (3-0-6), ARTIFICIAL INTELLIGENCE SERVICE DESIGN,
        06046424, ตรรกะและการแทนความรู้ 3 (3-0-6), LOGIC AND KNOWLEDGE REPRESENTATION,
        06046425, โมเดลแบบกำเนิด 3 (3-0-6), GENERATIVE MODEL,
        06046430, หัวข้อคัดสรรด้านปัญญาประดิษฐ์ 1 3 (3-0-6), SELECTED TOPICS IN ARTIFICIAL INTELLIGENCE 1,
        06046431, หัวข้อคัดสรรด้านปัญญาประดิษฐ์ 2 3 (3-0-6), SELECTED TOPICS IN ARTIFICIAL INTELLIGENCE 2,
        06046432, หัวข้อคัดสรรด้านปัญญาประดิษฐ์ 3 3 (3-0-6), SELECTED TOPICS IN ARTIFICIAL INTELLIGENCE 3,
        06046433, หัวข้อคัดสรรด้านปัญญาประดิษฐ์ 4 3 (3-0-6), SELECTED TOPICS IN ARTIFICIAL INTELLIGENCE 4,
        06046434, หัวข้อคัดสรรด้านปัญญาประดิษฐ์ 5 3 (3-0-6), SELECTED TOPICS IN ARTIFICIAL INTELLIGENCE 5,
        06046435, หัวข้อคัดสรรด้านปัญญาประดิษฐ์ 6 3 (3-0-6), SELECTED TOPICS IN ARTIFICIAL INTELLIGENCE 6}
    \i
\end{table}

</td></tr>
</table>

วท.บ.(สาขาวิชาเทคโนโลยีปัญญาประดิษฐ์) คณะเทคโนโลยีสารสนเทศ สจล.
<page_number>17</page_number>

---

\documentclass[120mm,168mm]{article}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{graphicx}

\usepackage{tikz}%&lt;&lt;&lt;&lt;&lt;&lt;&lt;
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt>&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&lt;&lt;&lt>&lt>&lt;&lt;&lt;&lt;&lt;&lt>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;
\usepackage{tikz-cd}
%&lt;&lt;&lt>&lt;&lt;&lt>&

---

\documentclass[120mm]{a4paper}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz-cd}

\usetikzlibrary {positioning}

\begin{document}

\begin{table}[h]
    \caption{แผนการศึกษา ปีที่ 1 ภาคการศึกษาที่ 1 (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง)} 
    \centering
    \begin{tr}
        <td>รหัสวิชา</td>
        <td>ชื่อวิชา</td>
        <td>หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง)</td>
    </tr>
    \foreach\x[count=\i] in{06046400, แคลคูลัส 1 CALCULUS 1, 3(3-0-6), 06046402, พีชคณิตเชิงเส้น LINEAR ALGEBRA, 3 (3-0-6), 06066000, คณิตศาสตร์ไม่ต่อเนื่อง DISCRETE MATHEMATICS, 3(3-0-6), 06066001, ความน่าจะเป็นและสถิติ PROBABILITY AND STATISTICS, 3 (3-0-6), 06066303, การแก้ปัญหาและการโปรแกรมคอมพิวเตอร์ PROGRAMMING AND COMPUTER PROGRAMMING, 3(2-2-5), 90641008, พื้นฐานทักษะการสื่อสารภาษาอังกฤษ INTRODUCTION TO ENGLISH COMMUNICATION SKILLS, 0 (0-0-45)}, \i}
    {
        <td>รวม</td>
        <td></td>
        <td>15</td>
    </tr>
\end{table}

\begin{table}[h]
    \caption{แผนการศึกษา ปีที่ 1 ภาคการศึกษาที่ 2 (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง)} 
    \centering
    \foreach\x[count=\i] in{06046401, แคลคูลัส 2 CALCULUS 2, 3(3-0-6), 06046403, การโปรแกรมคอมพิวเตอร์ COMPUTER PROGRAMMING, 3 (2-2-5), 06066301, โครงสร้างข้อมูลและอัลกอริทึม DATA STRUCTURES AND ALGORITHMS, 3(2-2-5), 06046404, พื้นฐานของระบบสมองกลฝังตัว FUNDAMENTAL OF EMBEDDED SYSTEM, 3 (3-0-6), 90641007, พลเมืองดิจิทัล DIGITAL CITIZEN, 3(3-0-6), 90641004, โครงงานกลุ่ม 1 TEAM-PROJECT 1, 1 (0-2-1), 9064xxxxx, วิชาเลือกหมวดวิชาศึกษาทั่วไป GENERAL EDUCATION COURSES, 3(x-x-x)}, \i}
    {
        <td>รวม</td>
        <td></td>
        <td>19</td>
    </tr>
\end{table}

วท.บ.(สาขาวิชาเทคโนโลยีปัญญาประดิษฐ์) คณะเทคโนโลยีสารสนเทศ สจล.
\end{document}

---

\documentclass[120mm]{a4paper}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
% \begin{document} เป็นคำอธิบายสำหรับหัวข้อหลัก
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt;&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt>&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt>&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt>&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt>&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt>&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt>&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt>&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt>&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt>&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt>&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts,graphicx,color}
\usepackage{tikz}%&lt;&lt;&lt>&lt;
% &lt;&lt;&lt;&lt; ตัวอย่างสัญลักษณ์ที่ใช้ในรูปแบบนี้
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amsfonts

---

\documentclass[120mm]{a4paper}
\usepackage{amsmath,amsfonts,graphicx,latexsym,color}
\usepackage{tikz-cd}

\usetikzlibrary {positioning}
\tikzset {
    &gt;={Latex[length=3pt]},
    myanglemark/.append style={
        angle radius = 1.5cm,
        inner sep = -0.25cm,
        outer sep = 0.8cm
    },
    myanglemark2/.append style={
        angle radius = 1.5cm,
        inner sep = -0.375cm,
        outer sep = 0.6cm
    }
}

\begin{document}
    
    \pagestyle[foot]{%&lt;&lt;&lt;
    \begin{table}[c] 
        \tr [td=2,th colspan="1"] {รหัสวิชา} [td=3,th colspan="1"] {ชื่อวิชา} [td=4,th colspan="1"] {หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง)} 
    \end{table}
    
    ปีที่ 3 ภาคการศึกษาที่ 1
    \begin{table}[c] 
        \tr [td=2,th colspan="1"] {รหัสวิชา} [td=3,th colspan="1"] {ชื่อวิชา} [td=4,th colspan="1"] {หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง)} 
    \end{table}
    
    06046415 การประมวลผลสัญญาณ SIGNAL PROCESSING 3 (3-0-6)
    06046414 การประมวลผลภาษาธรรมชาติด้วยการเรียนรู้อย่างเชิงลึก NATURAL LANGUAGE PROCESSING WITH DEEP LEARNING 3 (3-0-6)
    90642012 กระบวนการคิดเชิงออกแบบ DESIGN THINKING 3 (3-0-6)
    060464xx วิชาเลือกเทคโนโลยีปัญญาประดิษฐ์เฉพาะทาง ELECTIVE IN ARTIFICIAL INTELLIGENCE SPECIALIZATION 6 (3-0-6)
    06046440 วิชาสัมมนาปัญญาประดิษฐ์ SEMINAR IN ARTIFICIAL INTELLIGENCE 3 (2-2-5)
    \begin{table}[c] 
        \tr [td=1,th colspan="1"] {รวม} [td=4,th colspan="1"] {18}
    \end{table}
    
    \pagestyle[foot]{&lt;&lt;&lt;}
    \begin{table}[c] 
        \tr [td=2,th colspan="1"] {รหัสวิชา} [td=3,th colspan="1"] {ชื่อวิชา} [td=4,th colspan="1"] {หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง)} 
    \end{table}
    
    ปีที่ 3 ภาคการศึกษาที่ 2
    \begin{table}[c] 
        \tr [td=2,th colspan="1"] {รหัสวิชา} [td=3,th colspan="1"] {ชื่อวิชา} [td=4,th colspan="1"] {หน่วยกิต (บรรยาย-ปฏิบัติ-ศึกษาด้วยตนเอง)} 
    \end{table}
    
    060464xx วิชาเลือกเทคโนโลยีปัญญาประดิษฐ์เฉพาะทาง ELECTIVE IN ARTIFICIAL INTELLIGENCE SPECIALIZATION 6 (3-0-6)
    06046441 โครงงานเทคโนโลยีปัญญาประดิษฐ์ 1 PROJECT IN ARTIFICIAL INTELLIGENCE TECHNOLOGY 1 3 (0-9-0)
    90641006 โครงงานกลุ่ม 3 TEAM-PROJECT 3 1 (0-2-1)
    xxxxxxxxx วิชาเลือกเสรี 1 FREE ELECTIVE COURSE 1 3 (x-x-x)
    \begin{table}[c] 
        \tr [td=1,th colspan="1"] {รวม} [td=4,th colspan="1"] {13}
    \end{table}
    
\end{document}

วท.บ.(สาขาวิชาเทคโนโลยีปัญญาประดิษฐ์) คณะเทคโนโลยีสารสนเทศ สจล.

---

Extract all text from the image.

Instructions:
- Only return the clean Markdown.
- Do not include any explanation or extra text.
- You must include all information on the page.

Formatting Rules:
- Tables: Render tables using <table>...</table> in clean HTML format.
- Equations: Render equations using LaTeX syntax with inline ($...$) and block ($$...$$).
- Images/Charts/Diagrams: Wrap any clearly defined visual areas (e.g. charts, diagrams, pictures) in:

<figure>
Describe the image’s main elements (people, objects, text), note any contextual clues (place, event, culture), mention visible text and its meaning, provide deeper analysis when relevant (especially for financial charts, graphs, or documents), comment on style or architecture if relevant, then give a concise overall summary. Describe in Thai.
</figure>


- Page Numbers: Wrap page numbers in <page_number>...</page_number> (e.g., <page_number>14</page_number>).
- Checkboxes: Use ☐ for unchecked and ☑ for checked boxes.
