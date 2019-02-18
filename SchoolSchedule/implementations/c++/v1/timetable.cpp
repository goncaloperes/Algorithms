#include <stdio.h>
#include <memory.h>

using namespace std;

void swap(char& a, char &b){
	char d = b;
	b = a;
	a = d;
}

int hole(char v[6], bool flag){
	int s = 0;
	int cnt = 0;
	for(int i = 0; i < 6; i++){
		if(v[i] >= 0) cnt++;
		if(i && v[i] >= 0 && v[i - 1] == -1)
			s++;
	}
	if(cnt == 1)
		s += 1;
	if(flag)
		return s > 0;
	else
		return s;
}

int getholes(char v[5][6], bool flag){
	int sum = 0;
	for(int i = 0; i < 5; i++){
		sum += hole(v[i], flag);		
	}
	return sum;
}

struct state{
	char T[30][5][6];
	char C[30][5][6];
	int n, m;
	
	state(int m, int n): n(n), m(m){
		memset(T, -1, sizeof(T));
		memset(C, -1, sizeof(C));
	}
	
	bool setLession(int c, int t, int d, int l){
		if(T[t][d][l] >= 0)
			return false;
		if(C[c][d][l] >= 0)
			return false;
		
		T[t][d][l] = c;
		C[c][d][l] = t;
		return true;
	}
	
	bool tryToChangeLesson(int d1, int l1, int d2, int l2){
		
		for(int i = 0; i < m; i++){
			swap(C[i][d1][l1], C[i][d2][l2]);
		}
		
		for(int i = 0; i < n; i++){
			swap(T[i][d1][l1], T[i][d2][l2]);
		}
		
		return true;
	}
	
	bool tryToChangeTeacher(int t, int d1, int l1, int d2, int l2){
		int c1 = T[t][d1][l1];
		int c2 = T[t][d2][l2];
		
		
		
		if(c2 >= 0 && C[c2][d1][l1] >= 0)
			return false;
		if(c1 >= 0 && C[c1][d2][l2] >= 0)
			return false;
		if(c1 >= 0)
			C[c1][d1][l1] = -1;
		if(c2 >= 0)
			C[c2][d2][l2] = -1;
		
		swap(T[t][d1][l1], T[t][d2][l2]);
		
		if(c1 >= 0)
			C[c1][d2][l2] = t;
		if(c2 >= 0)
			C[c2][d1][l1] = t;
		return true;
	}

	bool tryToChangeClass(int c, int d1, int l1, int d2, int l2){
		int t1 = C[c][d1][l1];
		int t2 = C[c][d2][l2];
		
		if(t2 >= 0 && T[t2][d1][l1] >= 0)
			return false;
		if(t1 >= 0 && T[t1][d2][l2] >= 0)
			return false;
		
		if(t1 >= 0)
			T[t1][d1][l1] = -1;
		if(t2 >= 0)
			T[t2][d2][l2] = -1;
		
		swap(C[c][d1][l1], C[c][d2][l2]);
		
		if(t1 >= 0)
			T[t1][d2][l2] = c;
		if(t2 >= 0)
			T[t2][d1][l1] = c;
		return true;
	}
	
	int panelty(bool flag = false){
		
		int paneltyA = 0;
		int paneltyB = 0;
		int paneltyC = 0;
		
		for(int t = 0; t < n; t++) for(int d = 0; d < 5; d++){
			int ts = 0;
			for(int i = 0; i < 6; i++){
				if(T[t][d][i] >= 0) ts++;
			}
			if(ts > 4)
				paneltyA += ts - 4;
			
			for(int i = 0; i < 5; i++) for(int j = i + 1; j < 6; j++){
				if(T[t][d][i] >= 0 && T[t][d][i] == T[t][d][j]){
					paneltyB++;
				}
			}
				
		}
		
		for(int c = 0; c < m; c++) for(int d = 0; d < 5; d++){
			int ts = 0;
			for(int i = 0; i < 6; i++){
				if(C[c][d][i] >= 0) ts++;
			}
			if(ts > 4)
				paneltyA += ts - 4;

			for(int i = 0; i < 5; i++) for(int j = i + 1; j < 6; j++){
				if(C[c][d][i] >= 0 && C[c][d][i] == C[c][d][j]){
					paneltyB++;
				}
			}
		}
		
		int panelty = (paneltyA + paneltyB) * 100 + holes(flag);
		if(flag)
			printf("%d %d %d\n", paneltyA, paneltyB, panelty);
		
		return panelty;
	}
	
	
	
	int holes(bool flag){
		int sum = 0;
		for(int i = 0; i < n; i++)
			sum += getholes(T[i], flag);
		for(int i = 0; i < m; i++)
			sum += getholes(C[i], flag);
		return sum;
	}
	
	void print(){
		printf("Classes:\n");
		for(int i = 0; i < m; i++){
			printf("T%c", i + 'A');
			for(int j = 0; j < 5; j++){
				printf(" | ");
				for(int k = 0; k < 6; k++){
					char c = C[i][j][k] == -1 ? '.' : C[i][j][k] + 'A';
					printf("%c", c);
				}
			}
			puts("");
		}
		printf("Teachers:\n");
		for(int i = 0; i < n; i++){
			printf("P%c", i + 'A');
			for(int j = 0; j < 5; j++){
				printf(" | ");
				for(int k = 0; k < 6; k++){
					char c = T[i][j][k] == -1 ? '.' : T[i][j][k] + 'A';
					printf("%c", c);
				}
			}
			puts("");
		}
	}
};

int main(){
	freopen("G_he12t9p2a10s.txt", "r", stdin);
	int n, m;
	scanf("%d, %d", &m, &n);
	int l[30][30];
	memset(l, 0, sizeof(l));
	int x, y, z;
	while(scanf("%d, %d, %d", &x, &y, &z) == 3){
		l[x][y] = z;
	}
	
	state S(m, n);
	
	for(int i = 0; i < m; i++) for(int j = 0; j < n; j++){
		int c = l[i][j];
		//printf("%d %d %d\n", i, j, c);
		bool flag = 0;
		for(int p = 0; p < 5 && !flag; p++) for(int q = 0; q < 6 && !flag; q++){
			if(S.setLession(i, j, p, q)) c--;
			if(c == 0)
				flag = 1;
		}
		if(!flag){
			printf("err: %d %d %d\n", i, j, c);
		}
	}
	
	

	int panelty = S.panelty();
	
	while(1){
		bool imporved = false;
		state minS = S;
		for(int l = 0; l < 30; l++) for(int l1 = l + 1; l1 < 30; l1++){
			state S1 = S;
			if(S1.tryToChangeLesson(l / 6, l % 6, l1 / 6, l1 % 6) && S1.panelty() < panelty){
				//printf("l %d %d %d\n", l, l1, S1.panelty());
				imporved = true;
				minS = S1;
				panelty = S1.panelty();
			}
		}
		
		for(int c = 0; c < m; c++){
			for(int l = 0; l < 30; l++) for(int l1 = l + 1; l1 < 30; l1++){
				state S1 = S;
				if(S1.tryToChangeClass(c, l / 6, l % 6, l1 / 6, l1 % 6) && S1.panelty() < panelty){
					//printf("c %d %d %d\n", c, l, l1);
					imporved = true;
					minS = S1;
					panelty = S1.panelty();
				}
			}
		}

		for(int t = 0; t < n; t++){
			for(int l = 0; l < 30; l++) for(int l1 = l + 1; l1 < 30; l1++){
				state S1 = S;
				if(S1.tryToChangeTeacher(t, l / 6, l % 6, l1 / 6, l1 % 6) && S1.panelty() < panelty){
					//printf("t %d %d %d\n", t, l, l1);
					imporved = true;
					minS = S1;
					panelty = S1.panelty();
				}
			}
		}
		//printf("%d\n", panelty);
		S = minS;
		//S.print();break;
		if(!imporved) break;
	}

	printf("%d\n", S.panelty(true));
	S.print();
	
}
