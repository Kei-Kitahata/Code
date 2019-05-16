// FFT_image.cpp : コンソール アプリケーションのエントリ ポイントを定義します。
//

#include "stdafx.h"
#include <stdio.h>
#include <iostream>
#include <time.h>
#include <math.h>
#include <fstream>

#乱数解析をcsvに書き出し

using namespace std;


inline void InitRand()
{
	srand((unsigned int)time(NULL));
}

inline int randam_number()
{
	return rand();
}

int main()
{
	int i;

	InitRand();//毎回違う乱数にする
	int randam_list[1000];
	int sum = 0;
	ofstream log;//csvに書き出し用
	log.open("log.csv", ios::trunc);

	for (i = 0; i < 1000; i++) {//乱数リストを作成
		randam_list[i] = randam_number();
		sum = randam_list[i] + sum;
		log << randam_list[i] << std::endl;//csvに書き出し
	}
	log.close();

	//平均、分散、標準偏差を求める
	double average = sum / 1000;
	double variance = 0.0;
	double deviation = 0.0;
	for (i = 0; i < 1000; i++) {
		variance = (randam_list[i] - average)*(randam_list[i] - average);
	}


	variance = variance / 1000.0;
	deviation = sqrt(variance);

	std::cout << "average =" << average << ' ';
	std::cout << "varience =" << variance << ' ';
	std::cout << "devision =" << deviation << ' ';
	std::cout << std::flush;
	system("pause");
	return 0;
}
