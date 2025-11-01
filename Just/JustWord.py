#
# Just Right Word
# JustWord.py 2025/11/01
#
ILLUST_NO = -1  # 最初のイラスト(-1:ランダム)
WORDCHAIN_MODE = False  # しりとりモード
ENABLE_ALL_WORD = -1  # 全言葉入力可能（～-1:初回,0:なし,1～:1/nランダム）
CLIP = 1  # 0:dunnmy,1:lineclip

import pyxel
import pxt
import pwdic
import pim
import iras
if CLIP==1:  # lineclip
    import lineclip
else:  # CLIP==0:dummy
    pass

WIDTH = 344  # アプリ幅
TOP_Y = 4  # 上部メッセージＹ
TOP_XYWH = (4,TOP_Y, WIDTH-8,14)
LAST_Y = TOP_XYWH[1]+TOP_XYWH[3]  # 前回Ｙ
LASTIMG_SIZE = 50
LASTIMG_XYWH = (4,LAST_Y, LASTIMG_SIZE+2,LASTIMG_SIZE+2)  # 前回イラスト
LASTRANK_XYWH = [(4+LASTIMG_SIZE+2,LAST_Y, (WIDTH-LASTIMG_SIZE-2)//2-4,LASTIMG_SIZE+2),
        ((WIDTH+LASTIMG_SIZE+2)//2,LAST_Y, (WIDTH-LASTIMG_SIZE-2)//2-4,LASTIMG_SIZE+2)]  # 前回ランク
MAIN_Y = LASTIMG_XYWH[1]+LASTIMG_XYWH[3]+4  # メインＹ
IMG_SIZE = 158
IMG_XYWH = (4,MAIN_Y, IMG_SIZE+2,IMG_SIZE+2)  # メインイラスト
IMG_DESC_XYWH = (4,IMG_XYWH[1]+IMG_XYWH[3], IMG_SIZE+2,15)  # イラスト説明文
INIT_XYWH = (IMG_SIZE+10,MAIN_Y, 126,15)  # 頭文字
RANK_DY = 41
RANK_XYWH = (IMG_SIZE+10,INIT_XYWH[1]+INIT_XYWH[3], WIDTH-IMG_SIZE-14,RANK_DY*3+2)  # ランク
AUTO_BTN_XYWH = (WIDTH-46,MAIN_Y, 42,19)  # オートボタン
IMG_BTN_XYWH = (IMG_SIZE+10,IMG_XYWH[1]+IMG_XYWH[3]-20, 60,19)  # イラスト変更ボタン
INIT_BTN_XYWH = (IMG_BTN_XYWH[0]+IMG_BTN_XYWH[2]+2,IMG_XYWH[1]+IMG_XYWH[3]-20, 54,19)  # 頭文字変更ボタン
RANK_BTN_XYWH = (INIT_BTN_XYWH[0]+INIT_BTN_XYWH[2]+2,IMG_XYWH[1]+IMG_XYWH[3]-20, 54,19)  # ランク更新ボタン
INPUT_Y = IMG_DESC_XYWH[1]+IMG_DESC_XYWH[3]  # 入力Ｙ
INPUT_MAX_CHARA = 32
INP_MEAN_XYWH = (36,INPUT_Y, INPUT_MAX_CHARA*8+16,28)  # 入力文字列の意味
INPUT_XYWH = (36,INP_MEAN_XYWH[1]+INP_MEAN_XYWH[3]-1, INPUT_MAX_CHARA*8+16,19)  # 入力枠
HEIGHT = INPUT_XYWH[1]+INPUT_XYWH[3]+27  # アプリ高さ
RET_BTN_XYWH = (WIDTH-32,INPUT_XYWH[1], 29,19)  #  RET（入力／確定）ボタン
BS_BTN_XYWH = (4,INPUT_XYWH[1]+23, 29,19)  # BS（削除）ボタン
TAB_BTN_XYWH = (WIDTH-32,INPUT_XYWH[1]+23, 29,19)  # TAB（候補）ボタン
CAND_LINE_BTN_XYWH = (INPUT_XYWH[0]+INPUT_XYWH[2]-22,INPUT_XYWH[1]+23, 22,19)  # 候補ライン変更ボタン
DEBUGMSG_LINE = (HEIGHT-7)//12  # デバッグログライン数
DEBUGMSG_XYWH = (2,2, WIDTH-3,12*DEBUGMSG_LINE+3)  # デバッグログ
BG_COL = pyxel.COLOR_NAVY
FRAME_COL = pyxel.COLOR_CYAN
NOTE_COL_CODE = pxt.YELLOW
MEAN_COL_CODE = pxt.ORANGE
INITIAL_LETTERS = [
        'ア','イ','ウヴ','エ','オ','カガ','キギ','クグ','ケゲ','コゴ','サザ','シジ','スズ','セゼ','ソゾ',
        'タダ','チヂ','ツヅ','テデ','トド','ナ','ニ','ヌ','ネ','ノ','ハバパ','ヒビピ','フブプ','ヘベペ','ホボポ',
        'マ','ミ','ム','メ','モ','ヤ','ユ','ヨ','ラ','リ','ル','レ','ロ','ワ']  # ヴヂヅ
ALL_LETTER = 'アイウヴエオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモヤユヨラリルレロワ'
CV_YOUSOKU = {'ァ':'ア','ィ':'イ','ゥ':'ウ','ェ':'エ','ォ':'オ','ャ':'ヤ','ュ':'ユ','ョ':'ヨ','ッ':'ツ','ヲ':'オ','ー':'',}

class App:
    def add_debuglog(self, txt, maxchar=83, indent='   '):  # デバッグログ
        oneline = ''
        char_n = 0
        for ch in txt:
            w = 1 if ord(ch)<=0x7f else 2
            if char_n+w>maxchar:
                self.debuglogs.append(oneline)
                if len(self.debuglogs)>DEBUGMSG_LINE:
                    self.debuglogs.pop(0)
                oneline = indent+ch
                char_n = len(indent)+w
            else:
                oneline += ch
                char_n += w
        if oneline:
            self.debuglogs.append(oneline)
            if len(self.debuglogs)>DEBUGMSG_LINE:
                self.debuglogs.pop(0)

    def form_rank_mean_txt(self, rank, score, read, note, mean, maxchar, maxline, usersc=False):  # rank(0～),score(～100.0)
        rank_col = pxt.WHITE if rank==0 else pxt.LIGHTBLUE if 0<rank<=2 else pxt.CYAN if 2<rank<=6 else pxt.DARKBLUE
        usersc_txt = ' ユーザー入力' if usersc and rank==self.user_rank else ''
        score_col = pxt.PINK if usersc and rank==self.user_rank else ''
        return rank_col+f'【{rank+1}位】'+score_col+f'{score:.1f} '+rank_col+'点'+usersc_txt+'\n'\
                +NOTE_COL_CODE+pwdic.form_txtbox(pwdic.form_notation(read,note),maxchar,1,'  ','…')+'\n'\
                +MEAN_COL_CODE+pwdic.form_txtbox(mean.rstrip('…※＃'),maxchar,maxline,'  ','…')

    def form_read2notemean(self, reading):  # テキスト形成：読み⇒表記／意味
        all_mean = pwdic.KANA_DIC[reading]
        if len(all_mean)>=4:  # 複数意味
            popup_txt = NOTE_COL_CODE+all_mean[2]+'*7: '+MEAN_COL_CODE+all_mean[3].rstrip('※＃')
            for i in range(4, len(all_mean)-1, 2):
                popup_txt += '\n'+NOTE_COL_CODE+all_mean[i]+'*7: '+MEAN_COL_CODE+all_mean[i+1].rstrip('＃')
        else:  # 単一意味
            popup_txt = MEAN_COL_CODE+all_mean[1].rstrip('＃')
        return popup_txt

    # ____________________________________________________________________________________________________ カーソル
    def in_cursor(self, xywh, dy=1):  # 範囲内1～／範囲外0
        for i in range(dy):
            if xywh[0]<=pyxel.mouse_x<xywh[0]+xywh[2] and xywh[1]+(xywh[3]*i)//dy<=pyxel.mouse_y<xywh[1]+(xywh[3]*(i+1))//dy:
                return i+1
        return 0

    def in_cursor_cand(self):  # 範囲内1～／範囲外0
        for i in range(len(self.pim.cands_xw[self.pim.cand_line])):
            if self.in_cursor((self.pim.cands_xw[self.pim.cand_line][i][0]+36,INPUT_XYWH[1]+23, self.pim.cands_xw[self.pim.cand_line][i][1],19)):
                return i+1
        return 0

    # ____________________________________________________________________________________________________ ポップアップ
    def adjust_popup_xy(self, x, y, w, h):  # ポップアップ位置調整
        if x<4 or w+8>WIDTH:
            x = 4
        elif x+w+4>WIDTH:
            x = WIDTH-w-4
        if y<4 or h+8>HEIGHT:
            y = 4
        elif y+h+4>HEIGHT:
            y = HEIGHT-h-4
        return x,y

    def set_popup_txywh(self, txt, x, y, w, h):  # ポップアップ実行
        if txt:
            self.popup = True
            self.popup_txt = txt
            self.popup_x = x
            self.popup_y = y
            self.popup_w = w
            self.popup_h = h

    def popup_off(self):  # ポップアップ消去
        if self.popup:
            self.popup = False
            self.popup_txt = ''

    # ____________________________________________________________________________________________________ トップテキスト
    def set_top_txt(self, all_word=False):  # トップテキスト表示セット（self.top_txt, self.top_txt_x）
        if self.scores:
            n = len(self.scores)
            ave = sum(self.scores)/n
            this_last = '前回' if self.user_rank>9 else '今回'
            self.top_txt = f'  *6直近 {n} 回の平均 {ave:4.1f} 点     *7'+this_last+f'の得点 *E{self.scores[-1]:4.1f} *7点   *6これまでの最高得点 {self.high_score:4.1f} 点'
        elif all_word:
            self.top_txt = 'イラストに合う言葉を入力してね'
        else:
            self.top_txt = 'イラストに合う「'+'・'.join(list(self.pim.initial_letter))+'」から始まる言葉を入力してね'
        w_dot = pxt.textline(0,0, self.top_txt, txt_out=False)
        self.top_txt_x = TOP_XYWH[0]+(TOP_XYWH[2]-w_dot)//2
        self.set_toptxt_popup()  # トップテキストポップアップセット

    def set_toptxt_popup(self):  # トップテキストポップアップセット
        if self.scores:
            multi_scores = [('前回' if self.user_rank>9 else '今回')+f'の得点 {self.scores[-1]:4.1f} 点']
            for i,s in enumerate(self.scores[-2::-1]):
                multi_scores.append(f'    {i+1:2}つ前 {s:4.1f} 点')
            self.toptxt_popup_txt = '\n'.join(multi_scores)
        else:
            self.toptxt_popup_txt = ''
        characters,lines = pxt.textbox(0,0, self.toptxt_popup_txt, txt_out=False)
        self.toptxt_popup_x = TOP_XYWH[0]+TOP_XYWH[2]//2-characters*2
        self.toptxt_popup_y = TOP_XYWH[1]+TOP_XYWH[3]
        self.toptxt_popup_w = characters*4+4
        self.toptxt_popup_h = lines*12+3

    # ____________________________________________________________________________________________________ 前回イラスト
    def set_lastimg_popup(self):  # 前回イラストポップアップセット
        self.lastimg_popup_txt = self.img_description
        if self.lastimg_popup_txt:
            characters,lines = pxt.textbox(0,0, self.lastimg_popup_txt, txt_out=False)
            self.lastimg_popup_x = LASTIMG_XYWH[0]+LASTIMG_XYWH[2]//2-characters*2
            self.lastimg_popup_y = LASTIMG_XYWH[1]+LASTIMG_XYWH[3]
            self.lastimg_popup_w = characters*4+4
            self.lastimg_popup_h = lines*12+3
            self.lastimg_popup_x,self.lastimg_popup_y = self.adjust_popup_xy(self.lastimg_popup_x,self.lastimg_popup_y,self.lastimg_popup_w,self.lastimg_popup_h)

    # ____________________________________________________________________________________________________ 前回ランク
    def cls_lastrank(self):  # 前回ランク表示クリア
        self.lastrank_txt = ['']*2  # 前回ランク表示
        self.lastrank_popup_txt = ['']*2  # 前回ランクポップアップ
        self.lastrank_popup_x = [0]*2
        self.lastrank_popup_y = [0]*2
        self.lastrank_popup_w = [0]*2
        self.lastrank_popup_h = [0]*2

    def set_lastrank_popup(self, n, reading):  # 前回ランクポッポアップセット
        self.lastrank_popup_txt[n] = ''
        if reading:
            self.lastrank_popup_txt[n] = self.form_read2notemean(reading)
            characters,lines = pxt.textbox(0,0, self.lastrank_popup_txt[n], txt_out=False)
            self.lastrank_popup_x[n] = LASTRANK_XYWH[n][0]+6
            self.lastrank_popup_y[n] = LASTRANK_XYWH[n][1]+24
            self.lastrank_popup_w[n] = characters*4+4
            self.lastrank_popup_h[n] = lines*12+3
            self.lastrank_popup_x[n],self.lastrank_popup_y[n] = \
                    self.adjust_popup_xy(self.lastrank_popup_x[n],self.lastrank_popup_y[n],self.lastrank_popup_w[n],self.lastrank_popup_h[n])

    def set_lastrank_set_popup(self):  # 前回ランク表示セット＆ポップアップセット
        self.lastrank_txt[0] = self.form_rank_mean_txt(0,self.score10[0]*100,self.reading10[0],
                self.notation10[0],self.meaning10[0],33,2,usersc=True)  # 1位表示
        self.set_lastrank_popup(0, self.reading10[0])  # 1位ポップアップセット
        next_rank = self.user_rank if 0<self.user_rank<10 else 1
        self.lastrank_txt[1] = self.form_rank_mean_txt(next_rank,self.score10[next_rank]*100,self.reading10[next_rank],
                self.notation10[next_rank],self.meaning10[next_rank],33,2,usersc=True)  # 2位以下表示
        self.set_lastrank_popup(1, self.reading10[next_rank])  # 2位以下ポップアップセット

    # ____________________________________________________________________________________________________ メインイラスト
    def load_img_set_popup(self, post_num=-1):  # イラスト読み込み＆ポッポアップセット
        for i in range(3):
            desc = self.irasutoya.random_image_title((IMG_XYWH[2]-2,IMG_XYWH[3]-2), 7, post_num)
            self.img_popup_txt = f'No.{self.irasutoya.random_post_number:<5} {desc}'
            print(self.img_popup_txt)
            self.add_debuglog('≫ '+self.img_popup_txt)
            if self.irasutoya.error_code:
                self.add_debuglog(f'         ⇒ 画像読み込み失敗{i+1} エラー{self.irasutoya.error_code}')
                self.irasutoya.error_code=0
                continue
            else:
                break
        else:
            self.add_debuglog('         ⇒ 画像なし')
            self.auto_mode = False
        self.img_description = self.irasutoya.amend_title(desc)
        print('         '+self.img_description)
        self.add_debuglog('         ⇒ '+self.img_description)
        characters,lines = pxt.textbox(0,0, self.img_popup_txt, txt_out=False)
        self.img_popup_x = IMG_XYWH[0] if characters>(IMG_SIZE+2)//4 else IMG_XYWH[0]+IMG_XYWH[2]//2-characters*2
        self.img_popup_y = IMG_XYWH[1]+IMG_XYWH[3]
        self.img_popup_w = characters*4+4
        self.img_popup_h = lines*12+3

    # ____________________________________________________________________________________________________ 説明文
    def get_all_meanings(self, txt):  # 説明文からすべての意味
        low_txt = txt.lower()
        all_meanings = []
        for reading,value in pwdic.KANA_DIC.items():
            if len(value)>=4:  # 意味が複数
                if reading==txt:  # 読みと一致⇒すべての表記と意味を登録
                    for i in range(2, len(value)-1, 2):
                        all_meanings.append([reading, value[i], value[i+1].rstrip('＃')])  # 複数（読み,表記,意味）
                        all_meanings.append([value[i], reading, value[i+1].rstrip('＃')])  # 複数（表記,読み,意味）
                        #self.add_debuglog('   '+value[i]+' : '+value[i+1])
                else:
                    if reading in txt:  # 読みが含まれる⇒すべての表記と意味を登録
                        for i in range(2, len(value)-1, 2):
                            all_meanings.append([reading, value[i], value[i+1].rstrip('＃')])  # 複数（読み,表記,意味）
                            all_meanings.append([value[i], reading, value[i+1].rstrip('＃')])  # 複数（表記,読み,意味）
                    for i in range(2 if len(value)>=4 else 0, len(value)-1, 2):
                        for notation in value[i].split('・'):
                            if notation.lower() in low_txt:  # 表記（・区切り）が含まれる
                                all_meanings.append([reading, notation, value[i+1].rstrip('＃')])  # 複数（読み,表記,意味）
            else:  # 意味が１つ
                if reading==txt:  # 読みと一致
                    all_meanings.append([reading, value[0], value[1].rstrip('＃')])  # 複数（読み,表記,意味）
                    all_meanings.append([value[0], reading, value[1].rstrip('＃')])  # 複数（表記,読み,意味）
                else:
                    if reading in txt:  # 読みが含まれる＋表記が英文
                        all_meanings.append([reading, value[0], value[1].rstrip('＃')])  # 複数（読み,表記,意味）
                        all_meanings.append([value[0], reading, value[1].rstrip('＃')])  # 複数（表記,読み,意味）
                    for notation in value[0].split('・'):
                        if notation.lower() in low_txt:  #  表記（・区切り）が含まれる
                            all_meanings.append([reading, notation, value[1].rstrip('＃')])  # 複数（読み,表記,意味）
        txt_each_pos = [[] for _ in range(len(txt))]  # txtの文字位置に言葉と意味を
        for note_mean in all_meanings:
            start_pos = 0
            while True:
                if (idx := low_txt.find(note_mean[1].lower(), start_pos))==-1:
                    break
                txt_each_pos[idx].append(note_mean)
                start_pos = idx+1
        notain_maxlen = [max([len(note_mean[1]) for note_mean in ti]+[0]) for ti in txt_each_pos]  # txtの文字の位置に言葉の最長文字数
        multi_meanings = []
        separate_words_len = []
        pos = 0
        while pos<len(txt):
            maxlen = notain_maxlen[pos]
            separate_words_len.append(maxlen)
            meanings = set()  # 重複を除く
            for note_mean in txt_each_pos[pos]:
                if len(note_mean[1])==maxlen:
                    note = pwdic.form_notation(note_mean[0],note_mean[1])
                    meanings.add(NOTE_COL_CODE+note+'*7: '+MEAN_COL_CODE+note_mean[2])
            if maxlen:
                pos += maxlen
                multi_meanings.extend(meanings)
            else:
                pos += 1
        return '\n'.join(multi_meanings),separate_words_len

    def conv_colortxt(self, txt, word_len):  # 説明文カラー化
        base_color = pxt.WHITE
        color_seq = [pxt.LIME,pxt.YELLOW,pxt.LIGHTBLUE,pxt.PINK]
        color_n = 0
        color_txt = ''
        pos = 0
        for wl in word_len:
            if wl==0:
                color_txt += base_color+txt[pos:pos+1]
                pos += 1
            else:
                color_txt += color_seq[color_n]+txt[pos:pos+wl]
                pos += wl
                color_n = (color_n+1)%4
        return color_txt

    def set_imgdesc_popup(self, multi_meanings_txt):  # 説明文ポップアップセット
        if self.color_description:
            self.imgdesc_popup_txt = multi_meanings_txt
            characters,lines = pxt.textbox(0,0, self.imgdesc_popup_txt, txt_out=False)
            self.imgdesc_popup_x = IMG_DESC_XYWH[0]+IMG_DESC_XYWH[2]//2-characters*2
            self.imgdesc_popup_y = IMG_DESC_XYWH[1]+IMG_DESC_XYWH[3]
            self.imgdesc_popup_w = characters*4+4
            self.imgdesc_popup_h = lines*12+3
            self.imgdesc_popup_x,self.imgdesc_popup_y = self.adjust_popup_xy(self.imgdesc_popup_x,self.imgdesc_popup_y,self.imgdesc_popup_w,self.imgdesc_popup_h)

    # ____________________________________________________________________________________________________ 頭文字
    def set_initial_letter(self, all_word=False, ex_txt=''):  # 頭文字表示セット（self.initial_letter, self.disp_initials, self.fixed_txt, self.cands...）
        if all_word:
            self.pim.initial_letter = ALL_LETTER  # すべての文字
            self.disp_initials = 'すべての言葉'  # 頭文字
        else:
            tx_txt = ex_txt.translate(str.maketrans(CV_YOUSOKU))  # 促音拗音変換
            if tx_txt=='' or tx_txt[-1]=='ン':
                self.pim.initial_letter = pxt.pyxel_choice(INITIAL_LETTERS,5)  # ランダムな文字
            else:
                for letters in INITIAL_LETTERS:
                    if tx_txt[-1] in letters:
                        self.pim.initial_letter = letters  # 最後の文字
                        break
                else:
                    self.pim.initial_letter = pxt.pyxel_choice(INITIAL_LETTERS,5)  # ランダムな文字
            self.disp_initials = '「'+'・'.join(list(self.pim.initial_letter))+'」から始まる言葉'  # 頭文字
        self.pim.fixed_txt = self.pim.initial_letter[0] if len(self.pim.initial_letter)==1 else ''  # 確定テキスト
        self.pim.entering_txt = ''
        self.pim.set_candidate(self.pim.find_postfixes())  # 候補
        self.set_top_txt(all_word=all_word)  # トップテキスト

    def set_inittxt_popup(self):  # 頭文字ポップアップセット
        ranks = []
        for rank,(read,note,score) in enumerate(zip(self.reading10,self.notation10,self.score10)):
            (ranksc_col,ranknt_col) = (pxt.WHITE,pxt.YELLOW) if rank==0 else (pxt.LIGHTBLUE,pxt.YELLOW) if 0<rank<=2 else (pxt.CYAN,pxt.ORANGE) if 2<rank<=6 else (pxt.DARKBLUE,pxt.BROWN)
            ranks.append(ranksc_col+f'{rank+1:2}位 {score*100:4.1f}点: '+ranknt_col+pwdic.form_notation(read,note))
        self.inittxt_popup_txt = '\n'.join(ranks)
        characters,lines = pxt.textbox(0,0, self.inittxt_popup_txt, txt_out=False)
        self.inittxt_popup_x = INIT_XYWH[0]
        self.inittxt_popup_y = INIT_XYWH[1]+INIT_XYWH[3]
        self.inittxt_popup_w = characters*4+4
        self.inittxt_popup_h = lines*12+3
        self.inittxt_popup_x,self.inittxt_popup_y = self.adjust_popup_xy(self.inittxt_popup_x,self.inittxt_popup_y,self.inittxt_popup_w,self.inittxt_popup_h)

    # ____________________________________________________________________________________________________ ランク
    def clr_rank(self):  # ランククリア
        self.rank_txt = ['']*3  # ランク１～３位
        self.rank_reading,self.rank_notation,self.rank_meaning,self.rank_all_str = [],[],[],[]
        self.score10,self.reading10,self.notation10,self.meaning10,self.str10 = [],[],[],[],[]

    def set_rank_popup(self):  # ランクポップアップセット
        self.rank_popup_txt = ['']*3
        self.rank_popup_x = [0]*3
        self.rank_popup_y = [0]*3
        self.rank_popup_w = [0]*3
        self.rank_popup_h = [0]*3
        if self.reading10:
            for rank in range(3):
                self.rank_popup_txt[rank] = self.form_read2notemean(self.reading10[rank])
                characters,lines = pxt.textbox(0,0, self.rank_popup_txt[rank], txt_out=False)
                self.rank_popup_x[rank] = RANK_XYWH[0]+6
                self.rank_popup_y[rank] = RANK_XYWH[1]+RANK_DY*rank+24
                self.rank_popup_w[rank] = characters*4+4
                self.rank_popup_h[rank] = lines*12+3
                self.rank_popup_x[rank],self.rank_popup_y[rank] = self.adjust_popup_xy(self.rank_popup_x[rank],self.rank_popup_y[rank],
                        self.rank_popup_w[rank],self.rank_popup_h[rank])

    def set_new_words(self, rnd_n=10):  # 言葉セット
        match_fixed = []  # initial_letterから始まるすべての言葉
        for reading,value in pwdic.KANA_DIC.items():
            for le in self.pim.initial_letter:
                if reading[0]==le:
                    match_fixed.append([reading,value])
        for _ in range(min(rnd_n, len(match_fixed))):  # rnd_n個ランダム選択
            rnd = pxt.pyxel_choice(match_fixed,3)
            match_fixed.remove(rnd)
            self.rank_reading.append(rnd[0])
            self.rank_all_str.append(rnd[0])
            self.rank_notation.append(rnd[1][0])
            self.rank_all_str.append(rnd[1][0])
            self.rank_meaning.append(rnd[1][1].rstrip('…※＃'))
            self.rank_all_str.append(rnd[1][1].rstrip('…※＃'))

    def dummy_assoc_img_txts(self, txt):
        x = [pyxel.rndf(0,1) for _ in txt]
        total = sum(x)
        return [i/total for i in x]

    def set_ranking_words(self):  # 言葉ランキングセット
        if CLIP==1:  # lineclip
            all_scores = self.clip.assoc_img_txts(self.irasutoya.original_image, self.rank_all_str, scale=0.1)
        else:  # CLIP==0:dummy
            all_scores = self.dummy_assoc_img_txts(self.rank_all_str)
        best_strs = []
        best_scores = []
        for i in range(0, len(all_scores), 3):
            best_strs.append(max(zip(all_scores[i:i+3], self.rank_all_str[i:i+3]))[1])
        if CLIP==1:  # lineclip
            best_scores = self.clip.assoc_img_txts(self.irasutoya.original_image, best_strs, scale=0.1)
        else:  # CLIP==0:dummy
            best_scores = self.dummy_assoc_img_txts(best_strs)
        self.score10,self.reading10,self.notation10,self.meaning10,self.str10 = \
                zip(*sorted(zip(best_scores,self.rank_reading,self.rank_notation,self.rank_meaning,best_strs),reverse=True))
        for rank in range(3):
            self.rank_txt[rank] = self.form_rank_mean_txt(rank,self.score10[rank]*100,
                    self.reading10[rank],self.notation10[rank],self.meaning10[rank],41,1)

    def add_ranking_word(self, reading, notation, meaning):  # 新しい言葉追加
        if not reading in self.rank_reading:
            last_reading = self.reading10[-1]
            del_idx = self.rank_reading.index(last_reading)
            self.rank_reading.pop(del_idx)
            self.rank_notation.pop(del_idx)
            self.rank_meaning.pop(del_idx)
            del self.rank_all_str[del_idx*3:del_idx*3+3]
            self.rank_reading.append(reading)
            self.rank_all_str.append(reading)
            self.rank_notation.append(notation)
            self.rank_all_str.append(notation)
            self.rank_meaning.append(meaning.rstrip('…※＃'))
            self.rank_all_str.append(meaning.rstrip('…※＃'))

    def set_score(self, reading):  # 得点計算
        meanings = pwdic.KANA_DIC.get(reading)
        if meanings:
            notation = meanings[0]
            meaning = meanings[1]
        else:
            self.add_debuglog('要確認!! set_score(self, reading)')
            notation = '表記'
            meaning = '意味'
        self.add_ranking_word(reading, notation, meaning)  # 新しい言葉追加
        self.set_ranking_words()  # 言葉ランキングセット
        self.set_rank_popup()  # ランクポップアップセット
        self.set_inittxt_popup()  # 頭文字ポップアップセット
        self.user_rank = self.reading10.index(reading)  # 順位0～
        sc = self.score10[self.reading10.index(reading)]*100
        self.scores.append(sc)
        if len(self.scores)>5:
            self.scores.pop(0)
        if sc>self.high_score:
            self.high_score = sc

    # ____________________________________________________________________________________________________ 入力表示
    def set_inpmean_popup(self):  # 入力意味ポップアップ
        self.pim.inpmean_popup_txt = ''
        if self.pim.input_meaning:  # 入力テキストの意味あり
            self.pim.inpmean_popup_txt = self.form_read2notemean(self.pim.fixed_txt)
            characters,lines = pxt.textbox(0,0, self.pim.inpmean_popup_txt, txt_out=False)
            self.pim.inpmean_popup_x = INP_MEAN_XYWH[0]+1
            self.pim.inpmean_popup_y = INP_MEAN_XYWH[1]-lines*12-3 if lines>1 else INP_MEAN_XYWH[1]+12
            self.pim.inpmean_popup_w = characters*4+4
            self.pim.inpmean_popup_h = lines*12+3

    # ____________________________________________________________________________________________________ init
    def __init__(self):
        if CLIP==1:  # lineclip
            pyxel.init(WIDTH,HEIGHT, title='Just Right Word', display_scale=2, capture_scale=1, capture_sec=90)
            self.clip = lineclip.Association()
        else:  # CLIP==0:dummy
            pyxel.init(WIDTH,HEIGHT, title='Just Right Word (Random Score)', display_scale=2, capture_scale=1, capture_sec=90)
        pyxel.mouse(True)
        self.holddown = pxt.HoldDown()
        self.pim = pim.PyxelInputMethod()
        self.debuglogs = []
        reading,homonym,error = pwdic.simple_check()
        if error:
            self.add_debuglog('＞ 辞書 エラー : '+', '.join(error))
        else:
            self.add_debuglog(f'＞ 辞書 OK, 読み {reading}, 同音異義 {homonym}')
        self.irasutoya = iras.Irasutoya()
        if self.irasutoya.error_code:
            self.add_debuglog(f'＞ 接続エラー{self.irasutoya.error_code}')
        self.add_debuglog(f'＞ 全イラスト数 {self.irasutoya.total_posts}')
        self.auto_mode = False  # オートモード
        self.disp_log = False  # デバッグログ
        self.allword_cnt = ENABLE_ALL_WORD
        self.automode_cnt = 0
        self.popup = False  # ポップアップ
        self.top_txt = ''  # トップテキスト
        self.toptxt_popup_txt = ''  # トップテキストポップアップ
        self.scores = []  # 過去5回の得点
        self.high_score = 0  # ハイスコア
        pxt.cls_imagebank(1,col=BG_COL)  # 前回イラスト
        self.cls_lastrank()  # 前回ランク表示
        pxt.cls_imagebank(0,col=BG_COL)  # メインイラスト
        self.img_description = ''  # 元説明文
        self.color_description = ''  # 説明文
        self.disp_initials = ''  # 頭文字
        self.rank_txt = ['']*3  # 1～3位
        self.reloading_cnt = 30
        pyxel.run(self.update, self.draw) 

    # ____________________________________________________________________________________________________ update
    def update(self):
        if self.reloading_cnt:  # リロード中
            self.reloading_cnt -= 1
            if self.reloading_cnt==27:  # イラストコピー
                pxt.copy_imagebank(0,1)
                self.set_lastimg_popup()  # 前回イラストポップアップセット
                self.cls_lastrank()  # 前回ランク表示クリア
                if self.rank_txt[0]:
                    self.set_lastrank_set_popup()
            elif self.reloading_cnt==25:  # イラスト読み込み（ポップアップ）
                self.popup_txt = 'イラスト読み込み'
                characters,lines = pxt.textbox(0,0, self.popup_txt, txt_out=False)
                self.popup_w = characters*4+4
                self.popup_h = lines*12+3
                self.popup_x = IMG_XYWH[0]+(IMG_XYWH[2]-self.popup_w)//2
                self.popup_y = IMG_XYWH[1]+(IMG_XYWH[3]-self.popup_h)//2
                self.popup = True
            elif self.reloading_cnt==22:  # イラストクリア
                pxt.cls_imagebank(0,col=BG_COL)
                self.color_description = ''
            elif self.reloading_cnt==20:  # イラスト読み込み
                self.load_img_set_popup()
                multi_meanings_txt,separate_words_len = self.get_all_meanings(self.img_description)  # 説明文からすべての意味
                self.color_description = self.conv_colortxt(self.img_description, separate_words_len)  # 説明文カラー化
                self.set_imgdesc_popup(multi_meanings_txt)  # 説明文ポップアップセット
            elif self.reloading_cnt==17:  # 頭文字クリア
                self.disp_initials = ''
            elif self.reloading_cnt==15:  # 頭文字セット（ポップアップ）
                self.popup_txt = '頭文字設定'
                characters,lines = pxt.textbox(0,0, self.popup_txt, txt_out=False)
                self.popup_w = characters*4+4
                self.popup_h = lines*12+3
                self.popup_x = INIT_XYWH[0]+(INIT_XYWH[2]-self.popup_w)//2
                self.popup_y = INIT_XYWH[1]+(INIT_XYWH[3]-self.popup_h)//2
                self.popup = True
            elif self.reloading_cnt==10:  # 頭文字セット
                self.pim.input_meaning = ''  # 入力文字列の意味クリア
                self.pim.inpmean_popup_txt = ''
                if WORDCHAIN_MODE:
                    self.set_initial_letter(ex_txt=self.pim.fixed_txt)  # しりとりモード
                else:
                    if self.allword_cnt==0:
                        self.set_initial_letter()  # ランダム
                    elif self.allword_cnt>0:
                        self.set_initial_letter(all_word=(True if pyxel.rndi(1,self.allword_cnt)==1 else False))  # 全言葉／ランダム
                    else:
                        self.set_initial_letter(all_word=True)  # 全言葉
                        self.allword_cnt += 1

            elif self.reloading_cnt==7:  # ランキングクリア
                self.clr_rank()
            elif self.reloading_cnt==5:  # ランキングセット（ポップアップ）
                self.popup_txt = 'キーワード選定\nランキング設定'
                characters,lines = pxt.textbox(0,0, self.popup_txt, txt_out=False)
                self.popup_w = characters*4+4
                self.popup_h = lines*12+3
                self.popup_x = RANK_XYWH[0]+(RANK_XYWH[2]-self.popup_w)//2
                self.popup_y = RANK_XYWH[1]+(RANK_XYWH[3]-self.popup_h)//2
                self.popup = True
            elif self.reloading_cnt==0:  # ランキングセット
                self.set_new_words()  # 言葉セット
                self.set_ranking_words()  # 言葉ランキングセット
                self.set_rank_popup()  # ランクポップアップセット
                self.set_inittxt_popup()  # 頭文字ポップアップセット
                self.popup = False
            return

        if self.holddown.update():  # ボタン長押し
            self.disp_log = True  # デバッグログ表示
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if self.disp_log:  # デバッグログ消去
                self.disp_log = False
        elif pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            self.popup_off()  # ポップアップ消去
            if self.auto_mode:  # オートモードOFF
                self.auto_mode = False
            elif self.in_cursor(AUTO_BTN_XYWH):  # ボタン：オートモードON
                self.automode_cnt = -10
                self.auto_mode = True
            elif self.in_cursor(TOP_XYWH) and self.toptxt_popup_txt:  # トップテキスト
                self.set_popup_txywh(self.toptxt_popup_txt,self.toptxt_popup_x,self.toptxt_popup_y,self.toptxt_popup_w,self.toptxt_popup_h)
            elif self.in_cursor(LASTIMG_XYWH) and self.lastimg_popup_txt:  # 前回イラスト
                self.set_popup_txywh(self.lastimg_popup_txt,self.lastimg_popup_x,self.lastimg_popup_y,self.lastimg_popup_w,self.lastimg_popup_h)
            elif self.in_cursor(LASTRANK_XYWH[0]) and self.lastrank_popup_txt[0]:  # 前回１位
                self.set_popup_txywh(self.lastrank_popup_txt[0],self.lastrank_popup_x[0],self.lastrank_popup_y[0],self.lastrank_popup_w[0],self.lastrank_popup_h[0])
            elif self.in_cursor(LASTRANK_XYWH[1]) and self.lastrank_popup_txt[1]:  # 前回２位以下
                self.set_popup_txywh(self.lastrank_popup_txt[1],self.lastrank_popup_x[1],self.lastrank_popup_y[1],self.lastrank_popup_w[1],self.lastrank_popup_h[1])
            elif self.in_cursor(IMG_XYWH):  # イラスト
                self.set_popup_txywh(self.img_popup_txt,self.img_popup_x,self.img_popup_y,self.img_popup_w,self.img_popup_h)
            elif self.in_cursor(IMG_DESC_XYWH):  # 説明文
                self.set_popup_txywh(self.imgdesc_popup_txt,self.imgdesc_popup_x,self.imgdesc_popup_y,self.imgdesc_popup_w,self.imgdesc_popup_h)
            elif self.in_cursor(INIT_XYWH):  # 頭文字
                self.set_popup_txywh(self.inittxt_popup_txt,self.inittxt_popup_x,self.inittxt_popup_y,self.inittxt_popup_w,self.inittxt_popup_h)
            elif pos := self.in_cursor(RANK_XYWH,3):  # ランク
                pos -= 1
                self.set_popup_txywh(self.rank_popup_txt[pos],self.rank_popup_x[pos],self.rank_popup_y[pos],self.rank_popup_w[pos],self.rank_popup_h[pos])
            elif self.in_cursor(IMG_BTN_XYWH):  # ボタン：イラスト変更
                self.cls_lastrank()  # 前回ランク表示クリア
                self.user_rank = 99  # 前回のユーザーランク（99：ランク外）
                self.reloading_cnt = 30
            elif self.in_cursor(INIT_BTN_XYWH):  # ボタン：頭文字変更
                self.reloading_cnt = 20
            elif self.in_cursor(RANK_BTN_XYWH):  # 新しいランク
                self.reloading_cnt = 10
            elif self.in_cursor(INP_MEAN_XYWH) and self.pim.inpmean_popup_txt:  # 入力意味ポップアップ
                self.set_popup_txywh(self.pim.inpmean_popup_txt,self.pim.inpmean_popup_x,self.pim.inpmean_popup_y,self.pim.inpmean_popup_w,self.pim.inpmean_popup_h)
            elif self.in_cursor(BS_BTN_XYWH):  # BSボタン
                if self.pim.entering_txt or self.pim.fixed_txt:
                    if self.pim.backspace_btn():  # BSキー／ボタン：一文字削除
                        self.set_inpmean_popup()
            elif self.in_cursor(RET_BTN_XYWH):  # RETボタン
                if self.pim.entering_txt or self.pim.cand_n!=None or self.pim.input_meaning:
                    ret = self.pim.return_btn()  # RETキー／ボタン：確定
                    if ret==1:
                        self.set_inpmean_popup()
                    elif ret==3:
                        self.set_score(self.pim.fixed_txt)  # 得点計算
                        self.reloading_cnt = 30
            elif self.in_cursor(TAB_BTN_XYWH):  # TABボタン
                self.pim.right_key()
            elif len(self.pim.cands)>1 and self.in_cursor(CAND_LINE_BTN_XYWH):  # 候補ボタン
                self.pim.cand_line = (self.pim.cand_line+1) % len(self.pim.cands)
            elif self.pim.cands!=[[]] and (pos := self.in_cursor_cand()):  # 次の文字候補
                self.pim.fixed_txt += self.pim.cands[self.pim.cand_line][pos-1]
                self.pim.set_input_meaning()  # 入力文字列の意味セット
                self.set_inpmean_popup()
                self.pim.set_candidate(self.pim.find_postfixes())  # 候補文字列セット
                self.pim.entering_txt = ''
                self.pim.tab_cand_n = None

        if self.auto_mode:  # 60カウントごとに文字を変更、その2回ごとにイラストを変更
            self.automode_cnt += 1
            if self.automode_cnt%240==0:  # 新しいイラスト
                self.automode_cnt = 0
                self.cls_lastrank()  # 前回ランク表示クリア
                self.user_rank = 99  # 前回のユーザーランク（99：ランク外）
                self.reloading_cnt = 30
            elif self.automode_cnt%120==0:  # 新しい頭文字
                self.reloading_cnt = 20

        if pyxel.btnr(pyxel.KEY_RETURN):  # RETキー
            self.popup_off()  # ポップアップ消去
            if self.pim.return_btn()==3:  # RETキー／ボタン：確定
                self.set_score(self.pim.fixed_txt)  # 得点計算
                self.reloading_cnt = 30
        elif pyxel.btnp(pyxel.KEY_BACKSPACE,10,2):  # BSキー
            self.popup_off()  # ポップアップ消去
            self.pim.backspace_btn()  # BSキー／ボタン：一文字削除
        elif pyxel.btnp(pyxel.KEY_TAB,10,2) or pyxel.btnp(pyxel.KEY_SPACE,10,2) or pyxel.btnp(pyxel.KEY_RIGHT,10,2):  # TABキー｜SPCキー｜右キー
            self.popup_off()  # ポップアップ消去
            self.pim.right_key()
        elif pyxel.btnp(pyxel.KEY_LEFT,10,2):  # 左キー
            self.popup_off()  # ポップアップ消去
            self.pim.left_key()
        elif pyxel.btnp(pyxel.KEY_DOWN,10,2):  # 下キー
            self.popup_off()  # ポップアップ消去
            self.pim.down_key()
        elif pyxel.btnp(pyxel.KEY_UP,10,2):  # 上キー
            self.popup_off()  # ポップアップ消去
            self.pim.up_key()
        if sum(1 if ord(ch)<=0x7f else 2 for ch in self.pim.fixed_txt+self.pim.entering_txt)<INPUT_MAX_CHARA*2:
            if self.pim.any_key(pyxel.input_text):  # 文字入力(A～Z,a～z,-)
                self.set_inpmean_popup()

    # ____________________________________________________________________________________________________ draw
    def draw(self):
        pyxel.cls(BG_COL)
        if self.disp_log:
            pyxel.rect(*DEBUGMSG_XYWH, pyxel.COLOR_BLACK)  # デバッグログ（背景）
            pyxel.rectb(*DEBUGMSG_XYWH, FRAME_COL)  # デバッグログ（枠）
            for i,message in enumerate(self.debuglogs[-DEBUGMSG_LINE:]):
                pxt.textline(DEBUGMSG_XYWH[0]+2, DEBUGMSG_XYWH[1]+2+i*12, message, pyxel.COLOR_WHITE)  # デバッグログ
        else:
            if self.top_txt:
                pxt.textline(self.top_txt_x,TOP_XYWH[1], self.top_txt)  # トップテキスト
            pyxel.rectb(*LASTIMG_XYWH, FRAME_COL)  # 前回イラスト（枠）
            pyxel.blt(LASTIMG_XYWH[0]+1-(IMG_SIZE-LASTIMG_SIZE)//2,LASTIMG_XYWH[1]+1-(IMG_SIZE-LASTIMG_SIZE)//2, 1, 
                    0,0,IMG_SIZE,IMG_SIZE, scale=LASTIMG_SIZE/IMG_SIZE)  # 前回イラスト
            #pyxel.rect(LASTRANK_XYWH[0][0],LASTRANK_XYWH[0][1], 
            #       LASTRANK_XYWH[1][0]-LASTRANK_XYWH[0][0]+LASTRANK_XYWH[1][2],LASTRANK_XYWH[0][3], pyxel.COLOR_BLACK)  # 前回１位+２位以下（背景）
            pyxel.rectb(LASTIMG_XYWH[0],LASTIMG_XYWH[1], LASTIMG_XYWH[2]+LASTRANK_XYWH[0][2]+LASTRANK_XYWH[1][2],LASTIMG_XYWH[3], FRAME_COL)  # 前回イラスト+１位+２位以下（枠）
            #pyxel.rectb(*LASTRANK_XYWH[0], pyxel.COLOR_WHITE)  # 前回１位表示（枠）
            #pyxel.rectb(*LASTRANK_XYWH[1], pyxel.COLOR_GRAY)  # 前回２位以下表示（枠）
            if self.lastrank_txt[0]:
                pxt.textbox(LASTRANK_XYWH[0][0],LASTRANK_XYWH[0][1]+2, self.lastrank_txt[0], pyxel.COLOR_PINK if self.user_rank==0 else pyxel.COLOR_GRAY)  # 前回１位
            #pyxel.rectb(LASTRANK_XYWH[1][0],LASTRANK_XYWH[1][1], LASTRANK_XYWH[1][2],LASTRANK_XYWH[1][3], FRAME_COL)  # 前回２位以下（枠）
            if self.lastrank_txt[1]:
                pxt.textbox(LASTRANK_XYWH[1][0],LASTRANK_XYWH[1][1]+2, self.lastrank_txt[1], pyxel.COLOR_GRAY if self.user_rank==0 else pyxel.COLOR_WHITE)  # 前回２位以下
            pyxel.rect(*IMG_XYWH, pyxel.COLOR_WHITE)  # メインイラスト（背景）
            pyxel.rectb(*IMG_XYWH, FRAME_COL)  # メインイラスト（枠）
            pyxel.blt(IMG_XYWH[0]+1,IMG_XYWH[1]+1, 0, 0,0, IMG_SIZE,IMG_SIZE)  # メインイラスト
            if self.color_description:
                #pyxel.rectb(*IMG_DESC_XYWH, FRAME_COL)  # イラスト説明文（枠）
                characters,lines = pxt.textbox(0,0, self.color_description, txt_out=False)
                pxt.textbox(IMG_DESC_XYWH[0] if characters>(IMG_SIZE+2)//4 else IMG_DESC_XYWH[0]+IMG_DESC_XYWH[2]//2-characters*2,IMG_DESC_XYWH[1]+2, 
                        self.color_description)  # イラスト説明文
            #pyxel.rect(*INIT_XYWH, pyxel.COLOR_BLACK)  # 頭文字（背景）
            #pyxel.rectb(*INIT_XYWH, FRAME_COL)  # 頭文字（枠）
            pxt.textline(INIT_XYWH[0]+2,INIT_XYWH[1]+2,self.disp_initials,pyxel.COLOR_LIME)  # 頭文字
            #pyxel.rect(*RANK_XYWH, pyxel.COLOR_BLACK)  # ランク（背景）
            #pyxel.rectb(*RANK_XYWH, FRAME_COL)  # ランク（枠）
            for rank in range(3):
                if self.rank_txt[rank]:
                    pxt.textbox(RANK_XYWH[0],RANK_XYWH[1]+RANK_DY*rank+2, self.rank_txt[rank])  # ランク
            pyxel.elli(*AUTO_BTN_XYWH, pyxel.COLOR_RED if self.auto_mode else pyxel.COLOR_ORANGE if self.in_cursor(AUTO_BTN_XYWH) else pyxel.COLOR_NAVY)  # オートボタン（背景）
            pyxel.ellib(*AUTO_BTN_XYWH, pyxel.COLOR_LIGHT_BLUE if self.auto_mode else FRAME_COL)  # オートボタン（枠）
            pxt.textline(AUTO_BTN_XYWH[0]+10,AUTO_BTN_XYWH[1]+4, 'オート', 
                    pyxel.COLOR_WHITE if self.auto_mode or self.in_cursor(AUTO_BTN_XYWH) else pyxel.COLOR_GRAY)  # オートボタン
            pyxel.elli(*IMG_BTN_XYWH, pyxel.COLOR_ORANGE if self.in_cursor(IMG_BTN_XYWH) else pyxel.COLOR_NAVY)  # イラスト変更ボタン（背景）
            pyxel.ellib(*IMG_BTN_XYWH, FRAME_COL)  # イラスト変更ボタン（枠）
            pxt.textline(IMG_BTN_XYWH[0]+6,IMG_BTN_XYWH[1]+4, 'イラスト変更', pyxel.COLOR_WHITE if self.in_cursor(IMG_BTN_XYWH) else pyxel.COLOR_GRAY)  # イラスト変更ボタン
            pyxel.elli(*INIT_BTN_XYWH, pyxel.COLOR_ORANGE if self.in_cursor(INIT_BTN_XYWH) else pyxel.COLOR_NAVY)  # 頭文字変更ボタン（背景）
            pyxel.ellib(*INIT_BTN_XYWH, FRAME_COL)  # 頭文字変更ボタン（枠）
            pxt.textline(INIT_BTN_XYWH[0]+7,INIT_BTN_XYWH[1]+4, '頭文字変更', pyxel.COLOR_WHITE if self.in_cursor(INIT_BTN_XYWH) else pyxel.COLOR_GRAY)  # 頭文字変更ボタン
            pyxel.elli(*RANK_BTN_XYWH, pyxel.COLOR_ORANGE if self.in_cursor(RANK_BTN_XYWH) else pyxel.COLOR_NAVY)  # ランク変更ボタン（背景）
            pyxel.ellib(*RANK_BTN_XYWH, FRAME_COL)  # ランク変更ボタン（枠）
            pxt.textline(RANK_BTN_XYWH[0]+7,RANK_BTN_XYWH[1]+4, 'ランク変更', pyxel.COLOR_WHITE if self.in_cursor(RANK_BTN_XYWH) else pyxel.COLOR_GRAY)  # ランク変更ボタン
            if self.pim.input_meaning:
                #pyxel.rectb(*INP_MEAN_XYWH, FRAME_COL)  # 入力文字列の意味（枠）
                pxt.textbox(INP_MEAN_XYWH[0]+3, INP_MEAN_XYWH[1]+2, self.pim.input_meaning, pyxel.COLOR_WHITE)  # 入力文字列の意味
            pyxel.rect(*INPUT_XYWH, pyxel.COLOR_BLACK)  # 入力（背景）
            pyxel.rectb(*INPUT_XYWH, FRAME_COL)  # 入力（枠）
            x = 5
            x += pxt.textline(INPUT_XYWH[0]+x,INPUT_XYWH[1]+4, self.pim.fixed_txt, pyxel.COLOR_YELLOW if self.pim.input_meaning else pyxel.COLOR_WHITE)  # 確定入力文字列
            x += pxt.textline(INPUT_XYWH[0]+x,INPUT_XYWH[1]+4, self.pim.entering_txt, pyxel.COLOR_LIGHT_BLUE)  # 入力中文字列
            x += pxt.textline(INPUT_XYWH[0]+x,INPUT_XYWH[1]+4, '_' if pyxel.frame_count//20%2 else '', pyxel.COLOR_WHITE)  # 点滅入力カーソル
            if self.pim.entering_txt or self.pim.fixed_txt:
                pyxel.elli(*BS_BTN_XYWH, pyxel.COLOR_ORANGE if self.in_cursor(BS_BTN_XYWH) else pyxel.COLOR_NAVY)  # BS（削除）ボタン（背景）
                pyxel.ellib(*BS_BTN_XYWH, FRAME_COL)  # BS（削除）ボタン（枠）
                pxt.textline(BS_BTN_XYWH[0]+7,BS_BTN_XYWH[1]+4, '削除', pyxel.COLOR_WHITE if self.in_cursor(BS_BTN_XYWH) else pyxel.COLOR_GRAY)  # BS（削除）ボタン
            if self.pim.entering_txt or not self.pim.cand_n==None or self.pim.input_meaning:
                pyxel.elli(*RET_BTN_XYWH, pyxel.COLOR_ORANGE if self.in_cursor(RET_BTN_XYWH) else pyxel.COLOR_PURPLE 
                        if self.pim.input_meaning and not self.pim.entering_txt else pyxel.COLOR_NAVY)  # RET（入力／確定）ボタン（背景）
                pyxel.ellib(*RET_BTN_XYWH, FRAME_COL)  # RET（入力／確定）ボタン（枠）
                pxt.textline(RET_BTN_XYWH[0]+7,RET_BTN_XYWH[1]+4, '入力' if self.pim.entering_txt or not self.pim.cand_n==None else '確定', 
                        pyxel.COLOR_WHITE if self.in_cursor(RET_BTN_XYWH) else pyxel.COLOR_GRAY)  # RET（入力／確定）ボタン
            if not self.pim.cands==[[]]:
                pyxel.elli(*TAB_BTN_XYWH, pyxel.COLOR_ORANGE if self.in_cursor(TAB_BTN_XYWH) else pyxel.COLOR_NAVY)  # TAB（候補）ボタン（背景）
                pyxel.ellib(*TAB_BTN_XYWH, FRAME_COL)  # TAB（候補）ボタン（枠）
                pxt.textline(TAB_BTN_XYWH[0]+7,TAB_BTN_XYWH[1]+4, '候補', pyxel.COLOR_WHITE if self.in_cursor(TAB_BTN_XYWH) else pyxel.COLOR_GRAY)  # TAB（候補）ボタン
                for i,c in enumerate(self.pim.cands[self.pim.cand_line]):
                    xywh = (self.pim.cands_xw[self.pim.cand_line][i][0]+36,INPUT_XYWH[1]+23, self.pim.cands_xw[self.pim.cand_line][i][1],19)
                    pyxel.rect(*xywh, pyxel.COLOR_ORANGE if self.in_cursor(xywh) else pyxel.COLOR_GREEN if i==self.pim.cand_n else pyxel.COLOR_NAVY)  # 次カタカナ候補ボタン（背景）
                    pyxel.rectb(*xywh, FRAME_COL)  # 次カタカナ候補ボタン（枠）
                    pxt.textline(xywh[0]+6,xywh[1]+4, c, pyxel.COLOR_WHITE)  # 次カタカナ候補ボタン
                if len(self.pim.cands)>1:
                    pyxel.rect(*CAND_LINE_BTN_XYWH, pyxel.COLOR_ORANGE if self.in_cursor(CAND_LINE_BTN_XYWH) else pyxel.COLOR_NAVY)  # 候補ライン変更ボタン（背景）
                    pyxel.rectb(*CAND_LINE_BTN_XYWH, FRAME_COL)  # 候補ライン変更ボタン（枠）
                    pxt.textline(CAND_LINE_BTN_XYWH[0]+4,CAND_LINE_BTN_XYWH[1]+4, f'{self.pim.cand_line+1}／{len(self.pim.cands)}', 7)  # 候補ライン変更ボタン
        if self.popup and self.popup_txt:
            pyxel.rect(self.popup_x,self.popup_y,self.popup_w,self.popup_h, pyxel.COLOR_BLACK)  # ポップアップ（背景）
            pyxel.rectb(self.popup_x,self.popup_y,self.popup_w,self.popup_h, pyxel.COLOR_WHITE)  # ポップアップ（枠）
            pxt.textbox(self.popup_x+2,self.popup_y+2, self.popup_txt, pyxel.COLOR_YELLOW)  # ポップアップ

App()
