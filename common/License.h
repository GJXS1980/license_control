#ifndef __SNFACTORY_H__
#define __SNFACTORY_H__
 
// ANSC C/C++
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <cassert>
#include <vector>
 
#define MAX_LICENSE_SIZE 32
 
class CLicense
{
public:
	CLicense();
	CLicense(const CLicense& other);
	bool operator !=(const CLicense& other);
	bool operator ==(const CLicense& other);
 
	bool Create();
	bool encrypt();
	bool SerializeSource(const char* strFile, bool bStoring);
	std::string ToStringS() const;
	bool Serialize(const char* strFile, bool bStoring);
	std::string ToString() const;
	// added 2010.11.15
	void SetMacAddrType(int mMacType){m_nMacType = mMacType;} // 设置取物理地址类型
private:
	bool string_divide(std::vector<std::string> &_strlist, const std::string src, const std::string div);
protected:
	bool source_flag;
	char szMacAddress[128];
	unsigned char addr[6];
	unsigned char byMacAddrLen;
	//
	char m_szLicense[MAX_LICENSE_SIZE];
	int GetHDSN(char * szSN, int n);
	int m_nMacType;
};
 
#endif  /*__SNFACTORY_H__*/